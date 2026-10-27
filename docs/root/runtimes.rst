.. _root_runtimes:

Runtimes
========

Argenta is built on one idea: **the command layer and the interface are separate things**. A command — its trigger, flags, validation rules and handler — means the same regardless of whether a human types it into a terminal or a remote renderer fires it from a generated UI. Argenta draws a hard seam between the two and puts everything about *how commands are collected* and *how output is presented* on the other side, in a **runtime**.

This page explains how that seam is drawn and what it means for your application. It is a conceptual map — no API signatures, just the model the rest of the documentation assumes.

-----

The two sides of the seam
-------------------------

**Above the seam** lives everything your application *is*. None of it knows which runtime will consume it:

*   :ref:`Routers <root_api_router>` group commands into logical units.
*   :ref:`Commands <root_api_command_index>` declare triggers, :ref:`flags <root_flags>` (with :ref:`validation <root_api_command_possible_values>`) and descriptions.
*   Handlers implement the actual logic, receive a :ref:`Response <root_api_response>` and write output.
*   :ref:`DI providers <root_dependency_injection>` inject services into handlers.
*   :ref:`Behavior handlers <root_error_handling>` react to edge cases: unknown commands, empty input, bad flag syntax, the exit command.

**Below the seam** lives the runtime — the part that answers two questions: *where does input come from* and *where does output go*. Everything else — parsing, flag validation, DI, error handlers, the exit command — happens above the seam, identically for every runtime.

This is the core promise of the framework: **write the command layer once; the runtime is a deploy-time choice, not a design constraint**. Switching interfaces never touches a handler.

-----

What a runtime actually does
-----------------------------

Every runtime performs the same three duties:

1.  **Presents** — renders the startup surface (banner, startup messages, the command catalog) and every subsequent output block.
2.  **Collects** — obtains commands from wherever its interface lives: a typed line, a UI action, a network frame.
3.  **Dispatches** — hands each collected command to the same internal path, so flag validation, behavior handlers and the exit command behave identically everywhere.

A runtime is free to decide *everything else*: whether "input" is a prompt loop or a message queue, whether "output" is ANSI text or a JSON log entry, whether there is one user or many clients.

Blocks, not bytes
~~~~~~~~~~~~~~~~~

The application never formats output for a specific interface. It emits **semantic blocks** — a banner, a startup message, command output, a system message, a farewell — tagged by kind (:ref:`BlockKind <root_api_app_index>`). The runtime's *layout* decides what surrounds each block:

*   The REPL frames command output with dividing lines and inserts configured blank-line gaps.
*   The A2UI runtime turns each block into a structured log entry that the renderer lays out itself.

The same principle works in reverse: runtimes deliver commands, not keystrokes. Whether the command was typed as ``deploy --env prod --force`` or arrived as ``{"name": "deploy", "context": {"env": "prod", "force": true}}``, by the time it reaches your handler it is the same ``Response`` object with the same ``input_flags``.

The single dispatch path
~~~~~~~~~~~~~~~~~~~~~~~~

Because input and output both converge on shared contracts — ``InputCommand`` coming in, semantic blocks going out — **there is exactly one command-execution path in the framework**. Whatever reaches a handler has been parsed, validated and wrapped the same way; whatever a handler prints is captured as a block for the active layout. Adding a runtime cannot accidentally change how a command behaves, because a runtime simply cannot reach around that path.

-----

The shipped runtimes
--------------------

Two runtimes are built in. They are not special — they are simply the two concrete answers to "where do commands come from" that ship with the package.

.. list-table::
   :widths: 22 30 48
   :header-rows: 1

   * - Runtime
     - Input from
     - Output to
   * - :ref:`REPL <root_repl>`
     - typed lines in a prompt loop (``prompt_toolkit``, autocompletion)
     - terminal stdout, framed by the :ref:`terminal layout <root_api_repl>` (dividing lines, gaps)
   * - :ref:`A2UI <root_a2ui>`
     - ``action`` messages from renderers over a :ref:`transport <root_a2ui_transports>`
     - A2UI surface updates: a generated command UI plus a structured ``/log`` stream

The REPL is human-facing and synchronous: one user, one input line, blocking handlers. The A2UI runtime is interface-agnostic: input is any client that speaks the A2UI protocol (a browser, a native client, another process), output is machine-readable until a renderer draws it. An app that runs well in one generally runs in the other with zero changes — the caveats that exist are about interaction style, not registration (see each runtime's page).

-----

Choosing a runtime
------------------

The choice is made **at launch**, in the launcher — never inside the application code:

*   ``Orchestrator.run_repl(app)`` — the terminal session (delegates to A2UI when the process was started via ``argenta a2ui``).
*   ``Orchestrator.run_agent(app, transport)`` — the A2UI runtime over an explicit transport.
*   ``argenta repl`` / ``argenta a2ui`` — the CLI selects the runtime through :ref:`the environment bridge <root_a2ui>`, so the same ``main()`` serves both.

Because the choice is external, the same binary can expose the same commands through different interfaces for different environments — a developer terminal, a hosted web UI, a machine-driven subprocess — without a build matrix.

-----

Designed for more
-----------------

The runtime list is deliberately not closed. New runtimes are expected to arrive as the framework grows, and the architecture is what makes that possible without breaking your application:

*   **Runtimes are pluggable by construction.** A new runtime consumes the same contract — commands in, blocks out — and gains validation, DI, error handling and the exit command for free. Nothing on the command layer needs to change, including *your* code.
*   **The app can't leak interface assumptions.** Handlers emit text and read flags; they have no access to terminal control, sockets or rendering primitives. Anything a future runtime can express, your current handlers already produce.
*   **What a future runtime owns** is also defined: how input arrives, how each block kind is presented, and lifecycle (when the session starts, when the exit command ends it). That boundary is the extension point — it is where new interfaces plug in.

So when additional runtimes appear, they will show up as *additional launch options* — not migrations.

Writing your own
----------------

A custom runtime lives below the same seam: implement the :ref:`Layout <root_api_app_index>` protocol to receive output blocks (or accept the printer's output), collect commands however your interface works, and feed them through the application's dispatch. The seam is the contract — if you can turn user events into ``InputCommand`` objects and give blocks a place to land, you have a runtime. Embedding via ``MemoryTransport`` (:ref:`guide <root_a2ui_transport_memory>`) is a worked example of this shape: the agent runs in-process and a host application drives it.

-----

Where to go next
----------------

The documentation mirrors how an Argenta project is built:

1.  **Write the business logic** — commands, flags and handlers. Start at :ref:`Quick Start <root_quickstart>`, then :ref:`flags <root_flags>`, :ref:`error handling <root_error_handling>` and :ref:`dependency injection <root_dependency_injection>` as needed. All of it is runtime-agnostic.
2.  **Choose the runtime** — run the same app in the terminal (:ref:`REPL Runtime <root_repl>`) or expose it as an A2UI surface (:ref:`A2UI Runtime <root_a2ui>`), or build your own as described above.
