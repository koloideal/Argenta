.. _root_a2ui_transport_stdio:

Stdio Transport
===============

``StdioTransport`` speaks JSON Lines over the process's own stdin/stdout — the transport for when the agent is a subprocess and the client is its parent. Standard library only.

Wire format
-----------

*   Outbound: one JSON message per line on **stdout** — nothing else may write there. Diagnostics and ``--verbose`` logs go to **stderr** precisely to keep the wire clean.
*   Inbound: client writes one JSON object per line to the agent's **stdin**; each line is decoded and fed to the dispatch queue. EOF ends the session.
*   When stdout is a TTY, outgoing frames are indented for readability; piped stdout gets compact JSONL.

Usage
-----

.. code-block:: shell

    argenta a2ui app/main.py:main -t stdio

.. code-block:: python

   from argenta.a2ui import StdioTransport

   Orchestrator().run_agent(app, StdioTransport())

Parameters: ``out``/``inp`` (defaults ``sys.stdout``/``sys.stdin`` — overridable for embedding or tests), ``verbose``.

.. warning::
   An app running on stdio cannot also take interactive input: stdin is the protocol wire. Handlers calling ``input()`` will consume protocol frames — keep them out of apps you plan to run this way.

When to use
-----------

Parent-child setups: an orchestrator, editor plugin or wrapper that spawns the agent and talks to it over pipes — no ports, no sockets, no lifecycle to manage beyond the child's. For a renderer already running in a separate process with network access, :ref:`socket <root_a2ui_transport_socket>` is equivalent without sharing stdio.
