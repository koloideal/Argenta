.. _root_api_command_input_flag:

InputFlag
=========

The ``InputFlag`` object represents a flag entered by the user. It is created as a result of processing user input and contains information about the recognized flag: its name, prefix, value, and validation status.

.. seealso::

   Documentation for :ref:`Flag <root_api_command_flag>` — class for registering a flag.

   Documentation for :ref:`ValidationStatus <root_api_command_validation_status>` — flag validation statuses.

-----

.. warning ::
   Instances of this class are not intended for direct creation. They are contained in the :ref:`Response <root_api_response>` object.

**Attributes:**

.. py:attribute:: name
   :no-index:

   Name of the entered flag.

.. py:attribute:: prefix
   :no-index:

   Flag prefix: ``-``, ``--``, or ``---``.

.. py:attribute:: input_value

   Value passed with the flag. Can be ``''`` (empty string) for flags without values.

.. py:attribute:: status
   :no-index:

   Flag validation status: ``ValidationStatus.VALID``, ``ValidationStatus.INVALID``, or ``ValidationStatus.UNDEFINED``.

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

-----

Magic Methods
-------------

__str__
~~~~~~~

.. code-block:: python
   :linenos:

   __str__(self) -> str

Returns the string representation of the flag along with its value.

:return: String in the format ``flag value``.

**Usage example:**

.. literalinclude:: ../../../code_snippets/input_flag/snippet3.py
   :linenos:
   :language: python

-----

__repr__
~~~~~~~~

.. code-block:: python
   :linenos:

   __repr__(self) -> str

Returns the debug representation of the object.

:return: String in the format ``InputFlag<prefix=..., name=..., value=..., status=...>``.

**Usage example:**

.. literalinclude:: ../../../code_snippets/input_flag/snippet4.py
   :linenos:
   :language: python

-----

__eq__
~~~~~~

.. code-block:: python
   :linenos:

   __eq__(self, other: object) -> bool

Compares two entered flags for equality by name.

:param other: Object to compare.
:return: **True** if flag names match, otherwise **False**.

Two entered flags are considered equal if their names match.
