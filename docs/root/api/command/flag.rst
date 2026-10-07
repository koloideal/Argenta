.. _root_api_command_flag:

Flag
====

``Flag`` is an entity describing a command flag. Its main purpose is to define flag parameters, including its name, prefix, and validation rules.

.. seealso::

   Documentation for :ref:`PossibleValues <root_api_command_possible_values>` — an enumeration defining types of allowed values.
   
   Documentation for :ref:`InputFlag <root_api_command_input_flag>` — an object representing a processed flag entered by the user.
   
   :ref:`General information <root_flags>` about flags and their usage in ``Argenta``

-----

Initialization
--------------

.. code-block:: python
   :linenos:

   __init__(
       self, name: str, *,
       prefix: Literal["-", "--", "---"] = "--",
       possible_values: list[str] | Pattern[str] | PossibleValues = PossibleValues.ALL,
   ) -> None

Creates a new flag for registration in a command.

* ``name``: Flag name (required parameter).
* ``prefix``: Flag prefix (``-``, ``--``, ``---``). Defaults to ``--``.
* ``possible_values``: Value validation rules. Can be a list of strings, a regular expression, or a value from ``PossibleValues``. Defaults to ``PossibleValues.ALL``, meaning any value is allowed.

**Attributes:**

.. py:attribute:: name

   Flag name as a string.

.. py:attribute:: prefix

   Flag prefix. One of: ``"-"``, ``"--"``, ``"---"``.

.. py:attribute:: possible_values

   Allowed values for the flag.

**Usage example:**

.. literalinclude:: ../../../code_snippets/flag/snippet.py
   :linenos:
   :language: python

-----

Properties
----------

string_entity
~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   @property
   string_entity(self) -> str

Returns the string representation of the flag in the format ``prefix + name``.

:return: String representation of the flag

This property combines the prefix and name into a single string that represents the flag as it would appear on the command line.

-----

Magic Methods
-------------

__str__
~~~~~~~

.. code-block:: python
   :linenos:

   __str__(self) -> str

Returns the string representation of the flag (similar to ``string_entity``).

:return: String representation of the flag

**Usage example:**

.. literalinclude:: ../../../code_snippets/flag/snippet4.py
   :linenos:
   :language: python

-----

__repr__
~~~~~~~~

.. code-block:: python
   :linenos:

   __repr__(self) -> str

Returns the debug representation of the object.

:return: String in the format ``Flag<prefix=..., name=...>``.

**Usage example:**

.. literalinclude:: ../../../code_snippets/flag/snippet5.py
   :linenos:
   :language: python

-----

__eq__
~~~~~~

.. code-block:: python
   :linenos:

   __eq__(self, other: object) -> bool

Compares two flags for equality based on their string representation (``string_entity``).

:param other: Object to compare
:return: **True** if flags are equal, otherwise **False**

Two flags are considered equal if their ``string_entity`` are identical.

**Usage example:**

.. literalinclude:: ../../../code_snippets/flag/snippet6.py
   :linenos:
   :language: python

-----

.. _root_api_command_flag_predefined_flags:

PredefinedFlags
---------------

``argenta.command.PredefinedFlags``

The ``PredefinedFlags`` class provides a set of ready-made flags for use in applications without manual creation. These flags cover common scenarios.

All predefined flags are class attributes and represent ready-made ``Flag`` instances.

-----

Informational Flags
~~~~~~~~~~~~~~~~~~~


.. py:attribute:: PredefinedFlags.HELP

   Flag for displaying help: ``--help``
   
   * ``name``: ``"help"``
   * ``prefix``: ``"--"`` (default)
   * ``possible_values``: ``PossibleValues.NEITHER``

.. py:attribute:: PredefinedFlags.SHORT_HELP

   Short version of the help flag: ``-H``
   
   * ``name``: ``"H"``
   * ``prefix``: ``"-"``
   * ``possible_values``: ``PossibleValues.NEITHER``

.. py:attribute:: PredefinedFlags.INFO

   Flag for displaying information: ``--info``
   
   * ``name``: ``"info"``
   * ``prefix``: ``"--"`` (default)
   * ``possible_values``: ``PossibleValues.NEITHER``

.. py:attribute:: PredefinedFlags.SHORT_INFO

   Short version of the info flag: ``-I``
   
   * ``name``: ``"I"``
   * ``prefix``: ``"-"``
   * ``possible_values``: ``PossibleValues.NEITHER``

-----

Selection Flags
~~~~~~~~~~~~~~~

.. py:attribute:: PredefinedFlags.ALL

   Flag for selecting all items: ``--all``
   
   * ``name``: ``"all"``
   * ``prefix``: ``"--"``
   * ``possible_values``: ``PossibleValues.NEITHER``

.. py:attribute:: PredefinedFlags.SHORT_ALL

   Short version of the select all flag: ``-A``
   
   * ``name``: ``"A"``
   * ``prefix``: ``"-"``
   * ``possible_values``: ``PossibleValues.NEITHER``

-----

Network Flags
~~~~~~~~~~~~~

.. py:attribute:: PredefinedFlags.HOST

   Flag for specifying host IP address: ``--host``
   
   * ``name``: ``"host"``
   * ``prefix``: ``"--"`` (default)
   * ``possible_values``: Regular expression for IPv4 validation: ``r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"``

.. py:attribute:: PredefinedFlags.SHORT_HOST

   Short version of the host flag: ``-H``
   
   * ``name``: ``"H"``
   * ``prefix``: ``"-"``
   * ``possible_values``: Regular expression for IPv4 validation: ``r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"``

.. py:attribute:: PredefinedFlags.PORT

   Flag for specifying port: ``--port``
   
   * ``name``: ``"port"``
   * ``prefix``: ``"--"`` (default)
   * ``possible_values``: Regular expression for port validation: ``r"^\d{1,5}$"``

.. py:attribute:: PredefinedFlags.SHORT_PORT

   Short version of the port flag: ``-P``
   
   * ``name``: ``"P"``
   * ``prefix``: ``"-"``
   * ``possible_values``: Regular expression for port validation: ``r"^\d{1,5}$"``

-----

**Usage example:**

.. literalinclude:: ../../../code_snippets/flag/predefined_flags.py
   :linenos:
   :language: python
