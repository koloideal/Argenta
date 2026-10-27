.. _root_a2ui_transports_index:

Transports
==========

A transport carries A2UI messages in both directions: agent-to-renderer frames (surface and data-model updates) and renderer-to-agent ``action`` messages. Every transport implements the same :ref:`Transport <root_api_a2ui>` contract — ``send()``, ``actions()``, ``close()`` — so swapping transports never touches the application or the surface it emits.

Selecting one is a launch-time decision (``argenta a2ui -t <name>`` or the class passed to ``Orchestrator.run_agent``); the pages below document each wire format, its options and what a client needs to know to connect.

.. toctree::
   :maxdepth: 1

   sse
   websocket
   longpoll
   socket
   grpc
   stdio
   memory

Shared behavior
---------------

*   **History replay** — every server transport (SSE, WebSocket, long poll, socket, gRPC) keeps the sent messages and replays them to newly connected clients, so a renderer can attach at any time and rebuild the current surface.
*   **Multiple clients** — server transports broadcast each message to all connected clients; actions from any of them enter the single dispatch queue. All clients share one application session — there is no per-client state.
*   **Bound port** — the actual bound port is exposed as ``.port`` on every network transport (useful with ``port=0`` for an ephemeral port).
*   **Graceful shutdown** — when the exit action is dispatched or the process is interrupted, the runtime emits ``deleteSurface`` and closes the transport; client disconnects (including TCP resets) are treated as drops, not errors.
*   **Security** — none of the transports implement authentication or encryption. They bind to ``127.0.0.1`` by default and are designed for local use; for network exposure put them behind a proxy that terminates TLS and auth, or use :ref:`stdio <root_a2ui_transport_stdio>`/Unix sockets.

Writing a custom transport
--------------------------

``Transport`` is a protocol — any object with the three members works with ``run_agent``. A minimal implementation that prints outgoing frames and reads JSONL actions:

.. literalinclude:: ../../../code_snippets/a2ui/custom_transport.py
   :language: python
   :linenos:

Notes for transport authors:

*   ``send()`` is called for every outbound message; buffer if you must, but keep ordering — clients apply updates sequentially.
*   ``actions()`` is an iterator; when it ends (exhausted, client gone, transport closed) the agent shuts down and calls ``close()``.
*   ``close()`` must release whatever the transport holds — sockets, servers, queues — and is always called on exit, including after ``KeyboardInterrupt``.
