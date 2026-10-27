.. _root_a2ui_transport_memory:

Memory Transport
================

``MemoryTransport`` connects the agent to queues in the same process — no sockets, no ports. It exists for two jobs: **testing** the agent end-to-end and **embedding** it inside a host application that wants the surface but drives it itself. It is not selectable via ``argenta a2ui`` (there is nothing to connect to on the outside) — construct it in code.

Two modes
---------

**Script mode** (default) — deterministic, for tests:

.. code-block:: python

   transport = MemoryTransport(incoming=[
       {"action": {"name": "hello", "context": {}}},
       {"action": {"name": "q", "context": {}}},
   ])
   AgentRuntime(app, transport).run()
   # assert on transport.sent

``actions()`` replays ``incoming`` and ends; ``.sent`` records every message the agent emitted. The agent exits after the list is exhausted, so always end the script with the exit command if you want the full lifecycle (``deleteSurface``). See :ref:`Testing the A2UI agent <root_testing>` for a complete example.

**Live mode** (``live=True``) — for embedding:

.. code-block:: python

   transport = MemoryTransport(live=True)
   # run AgentRuntime(app, transport) on a thread, then:
   for message in transport.messages():      # outbound stream
       render(message)
   transport.push({"action": {"name": "deploy", "context": {"env": "prod"}}})
   transport.close()                          # ends messages() and the agent

``push()`` injects a client action; ``messages()`` is the outbound iterator the host consumes; ``close()`` terminates both.

Parameters: ``incoming`` — the script for script mode; ``live`` — switch between the two.

When to use
-----------

Anywhere you need the agent without a wire: pytest suites asserting on emitted frames, a desktop app embedding an Argenta tool, a harness driving the agent in-process. For anything crossing a process boundary use a real transport — :ref:`stdio <root_a2ui_transport_stdio>` or :ref:`socket <root_a2ui_transport_socket>` are the closest equivalents.
