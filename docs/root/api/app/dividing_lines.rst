.. _root_api_app_dividing_lines:

Dividing Lines
==============

Dividing lines in ``Argenta`` are used for visual structuring of output and separating information blocks from each other. The library offers two types of lines: static and dynamic.

-----

``StaticDividingLine``
----------------------

``StaticDividingLine`` creates a dividing line of **fixed** length. This type of line is useful for creating a predictable and unified interface.

.. code-block:: python
   :linenos:
   
      def __init__(self, unit_part: str = "-", *, 
                   length: int = 25) -> None

Creates a static dividing line instance.

* ``unit_part``: Character for building the line (only the first character is considered). Defaults to: ``-``.
* ``length``: Fixed line length. Defaults to: ``25``.

-----

``DynamicDividingLine``
-----------------------

``DynamicDividingLine`` creates a line whose length **dynamically** adjusts to the longest line in the command output. This requires capturing ``stdout``, resulting in dividers that perfectly frame the output content.

.. code-block:: python
  :linenos:

   __init__(self, unit_part: str = "-") -> None

Creates a dynamic dividing line instance.

* ``unit_part``: Character for building the line. Defaults to: ``-``.

Length is calculated automatically and is not set during initialization.

.. warning::
    Be sure to read about the nuances of using dynamic lines and capturing ``stdout`` in :ref:`this section<root_redirect_stdout>`.

-----

Purpose and Usage
-----------------

The choice between static and dynamic lines depends on your needs.

*   **StaticDividingLine** is ideal if:

    *   You need a strict and consistent design.
    *   You are using routers with disabled ``stdout`` capture (``disable_redirect_stdout=True``), where dynamic length calculation is not possible.

*   **DynamicDividingLine** (default behavior) is the preferred choice if:

    *   You want the interface to be adaptive.
    *   Your command output has varying lengths.
    *   Your handlers do not have interactive input operations (e.g., ``input()``).

The divider type for the entire application is set during ``App`` initialization via the ``dividing_line`` parameter.
