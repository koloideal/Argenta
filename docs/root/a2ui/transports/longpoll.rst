.. _root_a2ui_transport_longpoll:

Long-Poll Transport
===================

``LongPollTransport`` serves the agent over plain HTTP with request/response polling — the most conservative option, for networks where even SSE streams get buffered, timed out or cut by a proxy. Runs on the standard library alone.

Wire format
-----------

*   ``GET /`` — a human-readable index of the endpoints.
*   ``GET /events?after=<cursor>`` — long poll. If newer messages exist, answers immediately with ``{"messages": [...], "next": <cursor>}``; otherwise holds the request open up to ``poll_timeout`` (default 25 s) and then answers with an empty batch — the client reissues the poll with the returned ``next`` cursor. ``after=0`` replays the whole history.
*   ``POST /actions`` — the client-to-agent direction; body is one JSON object, accepted with ``202``.
*   ``OPTIONS`` — CORS preflight, ``Access-Control-Allow-Origin: *``.

Usage
-----

.. code-block:: shell

    argenta a2ui app/main.py:main -t poll -p 8080

.. code-block:: python

   from argenta.a2ui import LongPollTransport

   Orchestrator().run_agent(app, LongPollTransport(poll_timeout=15.0))

Parameters: ``host``/``port``, ``poll_timeout`` — how long an idle poll hangs before answering empty (longer = fewer roundtrips, slower disconnect detection; shorter = more traffic), ``verbose``. The bound port is on ``.port``.

When to use
-----------

Last-resort reachability: environments where persistent connections are unreliable or explicitly forbidden. It costs more requests than SSE but every exchange is an ordinary, cacheable-looking HTTP roundtrip that nothing can buffer forever.
