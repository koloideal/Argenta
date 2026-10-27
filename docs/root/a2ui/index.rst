.. _root_a2ui:

A2UI Runtime
============

Besides the interactive REPL, ``Argenta`` ships a second built-in runtime: the **A2UI runtime**. It exposes your application over `A2UI <https://a2ui.org/>`_ — a protocol where an agent (your app) streams a declarative description of a UI (a *surface*) to a renderer, and the renderer streams user actions back. The same commands you registered for the terminal become a generated UI in a browser, a terminal client or a native app: no UI code, no per-command wiring.

The split of responsibilities stays exactly where the framework puts it everywhere else:

*   **You** write routers, commands, flags and handlers — once.
*   **The runtime** turns the registered commands into a surface and dispatches incoming actions through the regular command-handling path.
*   **A renderer** (a browser client, a terminal client, a native app — anything that speaks A2UI) draws the components and sends actions back.

Because handlers go through the same dispatch path as in the REPL, everything documented for commands applies unchanged: :ref:`flags <root_flags>` arrive with their usual semantics, :ref:`DI <root_dependency_injection>` injection works, custom :ref:`error handlers <root_error_handling>` run, and ``print()`` output is captured and shown to the user.

-----

How it works
------------

When the agent starts, it emits the surface in three messages, then enters a dispatch loop:

1.  ``createSurface`` — declares the surface id, the component catalog (the set of component types the renderer knows how to draw) the renderer should use, and an optional theme.
2.  ``updateComponents`` — the component graph built from your registered routers (see :ref:`a2ui_surface`).
3.  ``updateDataModel`` — the initial data model the components bind to.

After that, for every client message carrying an ``action`` payload, the runtime builds an ``InputCommand`` — action ``name`` becomes the command trigger, ``context`` becomes the flags — and hands it to the same dispatch path the REPL uses. Handler output is captured into the log part of the data model, so the renderer simply re-renders when the model changes. When the :ref:`exit command <root_api_app_index>` is dispatched, the runtime emits ``deleteSurface`` and shuts the transport down.

Every message is a JSON object shaped as ``{"version": <protocol version>, "<kind>": {"surfaceId": <id>, ...}}``. The current implementation targets **A2UI protocol v0.9** with the *basic* component catalog.

-----

Running your app as an agent
----------------------------

The same ``main.py`` that starts the REPL can serve the agent. You pick the runtime at launch — the code stays identical.

With the CLI
~~~~~~~~~~~~

.. tip::
   To see the agent first, run the bundled demo from a repository checkout: ``argenta example a2ui agent`` starts the example agent, ``argenta example a2ui client`` serves the browser client on ``http://127.0.0.1:8080``. See :ref:`the example command <root_cli>`.

The recommended way is the ``argenta a2ui`` command from the ``[cli]`` extra:

.. code-block:: shell

    argenta a2ui app/main.py:main                          # SSE server on 127.0.0.1:8765
    argenta a2ui app/main.py:main --transport ws --verbose # WebSocket + lifecycle logging
    argenta a2ui app/main.py:main -t socket --socket-path /tmp/agent.sock
    argenta a2ui app/main.py:main --reload                 # restart on file changes

``argenta a2ui`` loads your entrypoint callable, sets the environment bridge (see below) and lets your ``main()`` run as usual — the ``Orchestrator.run_repl(app)`` call inside it transparently delegates to the A2UI runtime. Transport selection, port, socket path and verbosity are forwarded through environment variables, so **the application never knows which transport it runs on**.

All options and transports are documented in :ref:`the CLI section <root_cli>`.

.. note::
   ``sse``, ``poll``, ``socket`` and ``stdio`` run on the standard library alone. ``ws`` needs ``websockets`` and ``grpc`` needs ``grpcio`` + ``protobuf`` — install the ``[a2ui]`` extra to get both: ``uv add 'argenta[a2ui]'``.

Programmatically
~~~~~~~~~~~~~~~~

To embed the agent in your own process — a host application, a deployment wrapper, a test — call ``Orchestrator.run_agent`` with an explicit transport:

.. literalinclude:: ../../code_snippets/a2ui/run_agent.py
   :language: python
   :linenos:

``run_agent`` signature: ``(app, transport, config=None, *, verbose=False)``. It builds the DI container (including the :ref:`A2UI provider <root_api_a2ui>`), then runs :ref:`AgentRuntime <root_api_a2ui>` over your transport.

The environment bridge
~~~~~~~~~~~~~~~~~~~~~~

``argenta a2ui`` and ``Orchestrator.run_repl`` cooperate through environment variables described by :ref:`RunnerConfig <root_api_orchestrator_index>`:

*   ``ARGENTA_RUN_MODE=a2ui`` — tells ``run_repl`` to delegate to ``run_agent``.
*   ``ARGENTA_A2UI_TRANSPORT`` — the ``--transport`` value (``sse`` / ``ws`` / ``poll`` / ``socket`` / ``grpc`` / ``stdio``).
*   ``ARGENTA_A2UI_PORT`` / ``ARGENTA_A2UI_SOCKET_PATH`` / ``ARGENTA_A2UI_VERBOSE`` — transport options.
*   ``RUN_FROM_ARGENTA_RUNNER`` — set by both ``argenta repl`` and ``argenta a2ui``; makes ``ArgParser`` skip ``sys.argv`` parsing so CLI flags don't leak into your app.

An unknown or missing transport name falls back to ``stdio``. You can rename the variables or change defaults (host ``127.0.0.1``, port ``8765``) via ``Orchestrator(runner_config=RunnerConfig(...))``.

-----

.. _a2ui_surface:

The generated surface
---------------------

The runtime builds the component graph automatically — one card per command, one input per flag:

.. code-block:: text

    Column (root)
    ├── Card "a2ui_log_card"          — the output log (templated List over /log entries)
    ├── Text  (router title, h4)
    ├── Row   — up to cards_per_row command cards
    │   └── Card <command>
    │       ├── Text  (command description)
    │       ├── <flag input>          — one per registered flag
    │       └── Button "Run <command>" — fires the action
    ├── Text  (next router title)
    └── Row   ...

Flag-to-component mapping
~~~~~~~~~~~~~~~~~~~~~~~~~

The input rendered for a flag depends on its :ref:`possible_values <root_api_command_possible_values>`:

.. list-table::
   :widths: 35 20 45
   :header-rows: 1

   * - ``Flag`` declaration
     - Component
     - Value semantics
   * - ``possible_values=PossibleValues.NEITHER``
     - ``CheckBox``
     - toggle flag — no value; checked means "flag passed"
   * - ``possible_values=[...]`` (an iterable of values)
     - ``ChoicePicker``
     - single choice from the allowed values
   * - ``possible_values=re.compile(...)``
     - ``TextField``
     - free text; the regex is forwarded as ``validationRegexp`` so the renderer validates client-side too
   * - default (no restriction)
     - ``TextField``
     - free text

The data model
~~~~~~~~~~~~~~

The initial ``updateDataModel`` (written at path ``/``) contains a ``forms`` object — one entry per command trigger, with defaults per flag — and the empty ``log``:

.. code-block:: json

    {
      "forms": {"deploy": {"env": [], "force": false, "tag": ""}},
      "log": []
    }

Flag defaults match the bound component: ``false`` for checkboxes, ``[]`` for choice pickers, ``""`` for text fields. Flag values live at ``/forms/<trigger>/<flag_name>`` (escaped per RFC 6901 — ``~`` becomes ``~0``, ``/`` becomes ``~1``), which is exactly what each button's action context binds to — the renderer resolves the bindings and sends concrete values back.

The output log
~~~~~~~~~~~~~~

There is no terminal in agent mode, so every block the app emits — banner, startup messages, command output, system messages, handler tracebacks — is captured into a structured log entry appended to ``/log``:

.. code-block:: json

    {"id": 3, "kind": "output", "text": "Hello, world!", "markdown": "````\nHello, world!\n````"}

``kind`` is the semantic block kind (``banner``, ``startup_messages``, ``command_groups``, ``output``, ``system``, ``farewell``, ``error``); ``markdown`` wraps the text in a code fence so renderers keep the monospace layout. The list is capped at ``A2UIConfig.max_log_entries`` (200 by default) and resent in full on every change — renderers lay entries out and scroll the output card themselves.

-----

Actions: from the renderer back to commands
-------------------------------------------

A client-to-agent action message looks like:

.. code-block:: json

    {"version": "v0.9", "action": {"name": "deploy", "context": {"env": "prod", "force": true}}}

*   ``name`` — the command trigger (matched case-insensitively, same as typed input).
*   ``context`` — flag values keyed by flag name. The runtime turns them into an ``InputCommand``: context values become :ref:`InputFlag <root_api_command_input_flag>` values, so the handler sees the same ``response.input_flags`` it would see in the REPL.

Special cases:

*   **Exit command** — an action whose name is the exit trigger (``q`` by default) runs the exit handler, then ends the dispatch loop; the runtime sends ``deleteSurface`` and closes the transport.
*   **Unknown action name** — routed to the unknown-command handler (default or your override), its output lands in the log.
*   **Handler exception** — the traceback is appended to the log as an ``error`` entry; the surface stays alive.
*   **Messages without a valid action** — ignored.

.. warning::
   Handlers that call ``input()`` have nothing to read from in agent mode — there is no stdin between the renderer and the command, and on the ``stdio`` transport stdin *is* the protocol wire. Such commands will block the dispatch loop. Keep them on routers meant for the REPL, or rephrase the interaction as flags.

-----

.. _root_a2ui_transports:

Transports
----------

The transport carries JSON messages in both directions. All shipped implementations are interchangeable — pick by where your renderer lives. Each has a dedicated page with wire format, options and client notes; the choice matrix:

.. list-table::
   :widths: 12 22 30 36
   :header-rows: 1

   * - ``-t``
     - Transport
     - Wire format
     - Best for
   * - ``sse``
     - :ref:`SSETransport <root_a2ui_transport_sse>`
     - HTTP: ``GET /events`` stream + ``POST /actions``
     - **Default.** Browser clients, pure stdlib.
   * - ``ws``
     - :ref:`WebSocketTransport <root_a2ui_transport_websocket>`
     - WebSocket, one JSON message per frame
     - Browser clients; needs ``argenta[a2ui]``.
   * - ``poll``
     - :ref:`LongPollTransport <root_a2ui_transport_longpoll>`
     - HTTP: ``GET /events?after=<cursor>`` + ``POST /actions``
     - Proxies that buffer or cut long-lived responses.
   * - ``socket``
     - :ref:`SocketTransport <root_a2ui_transport_socket>`
     - JSON Lines over TCP or a Unix socket
     - Native/cross-process clients.
   * - ``grpc``
     - :ref:`GrpcTransport <root_a2ui_transport_grpc>`
     - gRPC bidi stream, one JSON message per ``Frame``
     - Native clients already speaking gRPC; needs ``argenta[a2ui]``.
   * - ``stdio``
     - :ref:`StdioTransport <root_a2ui_transport_stdio>`
     - JSON Lines over stdin/stdout
     - Machine clients driving the agent as a subprocess.
   * - —
     - :ref:`MemoryTransport <root_a2ui_transport_memory>`
     - in-process queues
     - Tests and embedding; not selectable via the CLI.

All server transports (``ws``, ``sse``, ``poll``, ``socket``, ``grpc``) **replay message history to late joiners** — a client that connects after startup rebuilds the current surface. Defaults: host ``127.0.0.1``, port ``8765`` (override with ``--port`` or ``ARGENTA_A2UI_PORT``).

.. toctree::
   :maxdepth: 1
   :hidden:

   transports/index

-----

Configuring the agent
---------------------

``A2UIConfig`` controls the surface identity (``surface_id``, ``catalog_id``, ``protocol_version``), the component ids, the log (``log_model_path``, ``max_log_entries``, ``log_fence``), the layout (``cards_per_row``, ``text_component``) and an optional ``theme`` mapping forwarded in ``createSurface``.

.. code-block:: python
   :linenos:

   from argenta import App, Orchestrator
   from argenta.a2ui import A2UIConfig, SSETransport

   app = App(override_system_messages=True)
   config = A2UIConfig(cards_per_row=3, max_log_entries=500, theme={"primaryColor": "#0af"})
   Orchestrator().run_agent(app, SSETransport(), config)

Whichever way the runtime was launched — ``run_agent(app, transport, config)`` or ``argenta a2ui`` — the effective ``A2UIConfig`` is available to handlers via DI: declare ``config: FromDishka[A2UIConfig]`` in a handler signature. (See :ref:`dependency injection <root_dependency_injection>` for the ``FromDishka`` pattern.)

.. seealso::
   Field-by-field reference: :ref:`A2UIConfig <root_api_a2ui>`.

-----

Preparing an app for agent mode
-------------------------------

An ``App`` that already runs in the REPL works as an agent with zero changes, but a few adjustments make the surface cleaner:

*   ``override_system_messages=True`` — recommended. Rich markup (colors, FIGlet banners) is meaningless for non-terminal renderers; with this flag system messages are emitted as plain text.
*   **Command descriptions** — they render as the card caption; keep them informative.
*   **Router titles** — render as section headers on the surface.
*   ``input()`` in handlers — doesn't work (see the warning above); prefer flags.
*   ``repeat_command_groups_printing`` — irrelevant in agent mode: the surface itself is the always-visible command list.

-----

Clients and renderers
---------------------

Anything that implements the A2UI renderer side can drive your app. To write a minimal client:

1.  Connect and read messages until ``deleteSurface``; handle ``createSurface`` / ``updateComponents`` / ``updateDataModel`` (the server transports replay history, so connecting at any time is fine).
2.  Render the components your catalog supports; write user input into the data model at the bound paths.
3.  Send ``{"version": "v0.9", "action": {"name": <trigger>, "context": {<flag>: <value>}}}`` when the user activates a command.

Two reference clients ship in the repo:

*   ``examples/a2ui/lit_client`` — a Lit browser client with automatic ``ws → sse → poll`` fallback; serve it with ``argenta example a2ui client`` (on ``http://127.0.0.1:8080``).
*   ``examples/a2ui/grpc_client.py`` — a terminal gRPC client that prints the agent log and accepts ``<command> flag=value`` lines; run it with ``argenta example a2ui client grpc``.

.. warning::
   The shipped transports do not implement authentication or encryption — they bind to ``127.0.0.1`` by default and are meant for local use. Putting an agent on a network is on you: front it with a proxy that does TLS and auth, or use the Unix-socket/stdio transports.
