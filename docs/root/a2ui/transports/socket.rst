.. _root_a2ui_transport_socket:

Socket Transport
================

``SocketTransport`` speaks JSON Lines over a raw TCP connection or a Unix domain socket — the simplest option for native (non-browser) clients, cross-process renderers and container-to-container links. Standard library only.

Wire format
-----------

*   One JSON object per line, in both directions (UTF-8, ``\n``-terminated).
*   On connect, the server replays the full message history, then broadcasts live messages to all connected clients; client lines are decoded and fed to the dispatch queue.
*   Client disconnects — including TCP resets — are treated as drops, not errors.

Usage
-----

.. code-block:: shell

    argenta a2ui app/main.py:main -t socket -p 9000
    argenta a2ui app/main.py:main -t socket --socket-path /tmp/agent.sock

.. code-block:: python

   from argenta.a2ui import SocketTransport

   Orchestrator().run_agent(app, SocketTransport(port=9000))
   Orchestrator().run_agent(app, SocketTransport(path="/tmp/agent.sock"))

Parameters: ``host``/``port`` for TCP (defaults ``127.0.0.1:8765``); ``path=`` switches the transport to a Unix domain socket and ignores host/port; ``verbose``. For TCP the bound port is on ``.port``.

When to use
-----------

When the renderer is another process on the same machine or network — a TUI client, a system service, a sidecar. Unix sockets additionally get filesystem permissions for free. For a subprocess you spawn yourself, :ref:`stdio <root_a2ui_transport_stdio>` is simpler (no socket management at all).
