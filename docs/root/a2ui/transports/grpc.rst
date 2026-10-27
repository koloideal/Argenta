.. _root_a2ui_transport_grpc:

gRPC Transport
==============

``GrpcTransport`` serves the agent over a gRPC bidirectional stream — for native clients in ecosystems that already speak gRPC (Go, Java, Rust services; browsers cannot call gRPC directly).

.. note::
   Requires ``grpcio`` and ``protobuf``: ``uv add 'argenta[a2ui]'``.

Wire format
-----------

*   Service ``argenta.a2ui.AgentChannel``, method ``Channel`` (stream-stream); definition in ``src/argenta/a2ui/transport/grpc/agent.proto``.
*   Each ``Frame`` message carries one JSON A2UI message in its ``json`` field, in both directions.
*   On stream open, the server replays history, then forwards live messages; client frames are decoded and fed to the dispatch queue. Any client disconnect ends that stream only.
*   On shutdown the server stops with ``stop_timeout`` (default 10 s) bounding the wait.

Usage
-----

.. code-block:: shell

    argenta a2ui app/main.py:main -t grpc -p 8765

.. code-block:: python

   from argenta.a2ui.transport.grpc import GrpcTransport

   Orchestrator().run_agent(app, GrpcTransport(port=50051))

Parameters: ``host``/``port``, ``verbose``, ``stop_timeout``. The bound port is on ``.port``.

A working client ships in the repo: ``examples/a2ui/grpc_client.py`` streams the agent log to the terminal and accepts ``<command> flag=value`` lines as actions — run it with ``argenta example a2ui client grpc``.

When to use
-----------

When your renderer is a native client and your infrastructure already does gRPC — typed stubs, load balancing, interceptors, deadlines come free. For local-only clients, :ref:`socket <root_a2ui_transport_socket>` or :ref:`stdio <root_a2ui_transport_stdio>` are lighter.
