.. _root_a2ui_transport_sse:

SSE Transport
=============

``SSETransport`` serves the agent over plain HTTP: renderers subscribe to a `Server-Sent Events <https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events>`_ stream and post actions back as HTTP requests. It is the **default transport** (``argenta a2ui`` without ``-t``) and runs on the standard library alone — no extra dependencies.

Wire format
-----------

*   ``GET /`` — a human-readable index of the endpoints.
*   ``GET /events`` — the SSE stream. Each agent message is sent as an ``event: message`` frame with the JSON payload in ``data:``. History is replayed to every new subscriber before live frames.
*   ``POST /actions`` — the client-to-agent direction. Body is one JSON object; accepted with ``202``.
*   ``OPTIONS`` on both paths — CORS preflight; the transport answers ``Access-Control-Allow-Origin: *`` so a client served from a different origin (e.g. the Lit dev server on ``:8080``) connects without a proxy.

Usage
-----

.. code-block:: shell

    argenta a2ui app/main.py:main                    # sse is the default
    argenta a2ui app/main.py:main -t sse -p 8080

.. code-block:: python

   from argenta.a2ui import SSETransport

   Orchestrator().run_agent(app, SSETransport(port=8080))

Parameters: ``host``/``port`` (defaults ``127.0.0.1:8765``), ``verbose`` — request log to stderr. The bound port is on ``.port``.

When to use
-----------

Browser renderers without a WebSocket stack, or environments where the WS upgrade gets stripped (corporate proxies, some CDN rules). SSE gives you a clean server-push channel with automatic reconnect for free — every browser has it. For a fully locked-down path where even streaming responses get buffered, see :ref:`long polling <root_a2ui_transport_longpoll>`.
