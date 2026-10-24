.. _root_a2ui_transport_websocket:

WebSocket Transport
===================

``WebSocketTransport`` serves the agent over a real WebSocket server — the lowest-latency, most standard channel for browser renderers.

.. note::
   Requires the ``websockets`` package: ``uv add 'argenta[a2ui]'``.

Wire format
-----------

*   One JSON message per WebSocket text frame, in both directions.
*   On connect, the server replays the full message history, then registers the client for live broadcasts — a renderer attaching mid-session rebuilds the current surface.
*   Plain HTTP requests to the port (health probes, accidental GETs) are answered with ``426 Upgrade Required`` instead of hanging.

Usage
-----

.. code-block:: shell

    argenta a2ui app/main.py:main -t ws -p 8765

.. code-block:: python

   from argenta.a2ui.transport.websocket import WebSocketTransport

   Orchestrator().run_agent(app, WebSocketTransport(port=9000))

Parameters: ``host``/``port`` (defaults ``127.0.0.1:8765``), ``verbose``. The bound port is on ``.port`` (works with ``port=0`` for an ephemeral port).

When to use
-----------

The canonical choice for browser clients with bidirectional needs. If your renderer doesn't need to *receive* much beyond actions, SSE is equally fine and dependency-free; if you can't install ``websockets``, use :ref:`sse <root_a2ui_transport_sse>` or :ref:`long poll <root_a2ui_transport_longpoll>`.
