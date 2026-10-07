.. _root_api_command_possible_values:


PossibleValues
==============

``PossibleValues`` is an enumeration that defines special validation modes for flag values. ``PossibleValues`` is used in the ``possible_values`` parameter of the ``Flag`` class to specify whether a flag can accept values and what restrictions are imposed on them.

``PossibleValues`` contains two main values: ``NEITHER`` (for flags that cannot accept values) and ``ALL`` (for flags accepting any values). This enumeration is used together with string lists and regular expressions to create a flexible validation system.

.. note::
   The validation result is available through the ``status`` attribute of the ``InputFlag`` instance. For more details, see :ref:`here <root_api_command_input_flag>`.

.. seealso::

   Documentation for :ref:`Flag <root_api_command_flag>` — flag class using ``PossibleValues``.
   
   Documentation for :ref:`ValidationStatus <root_api_command_validation_status>` — validation result of the entered flag.
   
   :ref:`General information <root_flags>` about flags and their usage in the ``Argenta`` application

-----

NEITHER
~~~~~~~

.. code-block:: python
   :linenos:

   PossibleValues.NEITHER = 'NEITHER'

Indicates that the flag **should not** have a value.

Flags with this value work as boolean switches: their presence on the command line is information in itself. Attempting to pass a value to such a flag will result in a validation error.

**Examples of flags with** ``NEITHER``:

* ``--help`` — help flag
* ``--verbose`` — verbose output flag
* ``--force`` — forced execution flag
* ``-A`` / ``--all`` — select all items flag

**Usage example:**

.. literalinclude:: ../../../code_snippets/possible_values/neither.py
   :linenos:
   :language: python

-----

ALL
~~~

.. code-block:: python
   :linenos:

   PossibleValues.ALL = 'ALL'

Indicates that the flag can accept **any** value.

Flags with this value are universal and do not impose restrictions on the data passed. Validation will always be successful.

**Examples of flags with** ``ALL``:

* ``--message`` — arbitrary text message
* ``--name`` — arbitrary name

**Usage example:**

.. literalinclude:: ../../../code_snippets/possible_values/all.py
   :linenos:
   :language: python

-----

The possible_values Parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``PossibleValues`` is used as one of the possible types for the ``possible_values`` parameter when creating a ``Flag`` instance.

**Available types for** ``possible_values``:

1.  ``PossibleValues.NEITHER``: flag without a value.
2.  ``PossibleValues.ALL``: flag with any value (default).
3.  ``list[str]``: flag with a limited set of values.
4.  ``Pattern[str]``: flag with a value validated by a regular expression.

**Combined usage example:**

.. literalinclude:: ../../../code_snippets/possible_values/combined.py
   :linenos:
   :language: python
