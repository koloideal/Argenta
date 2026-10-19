.. _root_api_repl:

REPL Runtime
============

The REPL runtime runs an ``App`` as an interactive terminal session. Its presentation — the dividing line that frames command output and the blank-line gaps between blocks — belongs to the runtime, not to the ``App``: the same application can run as an A2UI agent, where the renderer lays out output on its own and no terminal decoration is emitted.

.. code-block:: python

   from argenta.repl import REPLConfig, StaticDividingLine, DynamicDividingLine

-----

``REPLConfig``
--------------

.. autoclass:: argenta.repl.REPLConfig

Passed to ``Orchestrator.run_repl``; every field documents itself via an ``Annotated[type, "..."]`` doc string in the source.

.. code-block:: python

   from argenta import App, Orchestrator
   from argenta.repl import DynamicDividingLine, REPLConfig

   app = App()
   Orchestrator().run_repl(app, REPLConfig(dividing_line=DynamicDividingLine("~")))

-----

``StaticDividingLine``
----------------------

``StaticDividingLine`` creates a dividing line of **fixed** length. This type of line is useful for creating a predictable and unified interface.

.. autoclass:: argenta.repl.StaticDividingLine

* ``unit_part``: Character for building the line (only the first character is considered). Defaults to: ``-``.
* ``length``: Fixed line length. Defaults to: ``25``.

-----

``DynamicDividingLine``
-----------------------

``DynamicDividingLine`` creates a line whose length **dynamically** adjusts to the longest line in the command output. This requires capturing ``stdout``, resulting in dividers that perfectly frame the output content.

.. autoclass:: argenta.repl.DynamicDividingLine

* ``unit_part``: Character for building the line. Defaults to: ``-``.
* ``min_length`` / ``max_length``: bounds for the computed length. Default to ``10`` and ``100``.

.. warning::
    Be sure to read about the nuances of using dynamic lines and capturing ``stdout`` in :ref:`this section<root_redirect_stdout>`.

-----

Purpose and Usage
-----------------

*   **StaticDividingLine** is ideal if:

    *   You need a strict and consistent design.
    *   You are using routers with disabled ``stdout`` capture (``disable_redirect_stdout=True``), where dynamic length calculation is not possible.

*   **DynamicDividingLine** is the preferred choice if:

    *   You want the interface to be adaptive.
    *   Your command output has varying lengths.
    *   Your handlers do not have interactive input operations (e.g., ``input()``).
