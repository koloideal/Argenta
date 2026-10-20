.. _root_api_a2ui:

A2UI Runtime
============

The ``argenta.a2ui`` package implements the agent side of `A2UI <https://a2ui.org/>`_: it renders the registered commands as a declarative surface and routes client actions back through the regular command dispatch path. The conceptual walkthrough lives in the :ref:`A2UI guide <root_a2ui>`; this page is the API reference.

.. code-block:: python

   from argenta.a2ui import (
       AgentRuntime,
       A2UIConfig,
       A2UIProvider,
       Transport,
       StdioTransport,
       MemoryTransport,
       SocketTransport,
       SSETransport,
       LongPollTransport,
   )

   from argenta.a2ui.transport.websocket import WebSocketTransport  # needs argenta[a2ui]
   from argenta.a2ui.transport.grpc import GrpcTransport          # needs argenta[a2ui]

-----

``AgentRuntime``
----------------

.. autoclass:: argenta.a2ui.AgentRuntime
   :members: run

The orchestration entry point is ``Orchestrator.run_agent(app, transport, config=None, *, verbose=False)`` (see :ref:`Orchestrator <root_api_orchestrator_index>`), which builds the DI container and runs this runtime. Instantiate ``AgentRuntime`` directly only when embedding without the orchestrator — for example in tests with ``MemoryTransport``.

Message types
~~~~~~~~~~~~~

.. code-block:: python

   from argenta.a2ui.models import JsonValue, Message

*   ``JsonValue`` — recursive JSON value type used across the package.
*   ``Message`` — ``dict[str, JsonValue]``; the unit exchanged by transports in both directions.

-----

``A2UIConfig``
--------------

.. autoclass:: argenta.a2ui.A2UIConfig

Frozen dataclass configuring the surface and the message envelope. Every field documents itself via an ``Annotated[type, "..."]`` doc string; the rendered signature above shows the bare field types and defaults.

``A2UIProvider``
----------------

.. autoclass:: argenta.a2ui.A2UIProvider

Dishka provider that serves the effective ``A2UIConfig`` from the container context (``APP`` scope). ``Orchestrator.run_agent`` registers it automatically; add ``custom_providers`` as usual on top of it. Handlers can depend on ``FromDishka[A2UIConfig]``.

-----

``Transport``
-------------

.. autoclass:: argenta.a2ui.Transport

The transport contract — three members:

*   ``send(message)`` — emit one agent-to-renderer message.
*   ``actions()`` — yield decoded client-to-agent messages; the iterator ending ends the agent.
*   ``close()`` — release the transport (sockets, servers, queues).

The runtime calls ``send`` for surface and log updates, iterates ``actions`` in its dispatch loop, and always calls ``close`` on exit.

-----

Stdlib transports
-----------------

The following transports depend only on the standard library.

``StdioTransport``
~~~~~~~~~~~~~~~~~~

.. autoclass:: argenta.a2ui.StdioTransport

JSON Lines over stdin/stdout — one JSON message per line in both directions. Meant for machine clients driving the agent as a subprocess: stdout carries the protocol, diagnostics go to stderr. When stdin is a TTY the transport warns — humans should use ``ws``/``sse`` with a real renderer.

``MemoryTransport``
~~~~~~~~~~~~~~~~~~~

.. autoclass:: argenta.a2ui.MemoryTransport
   :members: push, messages, close

In-memory transport for tests and embedding. Two modes:

*   **Script mode** (default): ``actions()`` replays the ``incoming`` preload and ends — feed a fixed action list and assert on ``.sent``.
*   **Live mode** (``live=True``): ``actions()`` stays open; the host injects actions via ``push()`` and subscribes to outgoing frames via ``messages()`` until ``close()``.

``SocketTransport``
~~~~~~~~~~~~~~~~~~~

.. autoclass:: argenta.a2ui.SocketTransport

JSON Lines over raw TCP (``host``/``port``) or a Unix domain socket (``path=``). Replays message history to late joiners; the actual bound port is available as ``.port``.

``SSETransport``
~~~~~~~~~~~~~~~~

.. autoclass:: argenta.a2ui.SSETransport

Serves the A2UI stream over HTTP Server-Sent Events (``GET /events``) and accepts actions via ``POST /actions``. Pure-stdlib; survives proxies that block WebSocket upgrades. Sends permissive CORS headers so a client served from another port can connect.

``LongPollTransport``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: argenta.a2ui.LongPollTransport

Long-polling variant of the HTTP transport: ``GET /events?after=<cursor>`` holds the request open until new messages arrive or ``poll_timeout`` (default 25 s) expires, then answers ``{"messages": [...], "next": <cursor>}``. For proxies that buffer or cut long-lived responses.

-----

Optional transports
-------------------

These require the ``[a2ui]`` extra (``uv add 'argenta[a2ui]'``) and are imported from their own modules rather than ``argenta.a2ui``:

``WebSocketTransport``
~~~~~~~~~~~~~~~~~~~~~~

.. py:class:: argenta.a2ui.transport.websocket.WebSocketTransport

   ``WebSocketTransport(host="127.0.0.1", port=8765, *, verbose=False)``

Broadcasts messages to every connected client and replays history to late joiners; the bound port is available as ``.port``. Plain HTTP requests to the port are answered with ``426 Upgrade Required``. Requires ``websockets``.

``GrpcTransport``
~~~~~~~~~~~~~~~~~

.. py:class:: argenta.a2ui.transport.grpc.GrpcTransport

   ``GrpcTransport(host="127.0.0.1", port=8765, *, verbose=False, stop_timeout=10)``

A2UI over a gRPC bidirectional stream ``argenta.a2ui.AgentChannel/Channel`` — one JSON message per ``Frame`` in both directions; the service definition is ``argenta/a2ui/transport/grpc/agent.proto``. For native clients already speaking gRPC (browsers cannot call gRPC directly). Requires ``grpcio`` and ``protobuf``; ``stop_timeout`` bounds the shutdown wait.
