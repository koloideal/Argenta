.. _root_api_command_validation_status:

ValidationStatus
================

``ValidationStatus`` is an enumeration that defines the validation state of a flag. Its purpose is to provide standard constants for displaying the validation result. ``ValidationStatus`` is used in the ``status`` attribute of the ``InputFlag`` class.

``ValidationStatus`` contains three values: **VALID** (valid flag), **INVALID** (invalid), and **UNDEFINED** (unregistered).

.. note::

   The validation status is set automatically when creating an ``InputFlag`` instance based on the rules defined in the corresponding ``Flag``.

.. seealso::

   Documentation for :ref:`InputFlag <root_api_command_input_flag>` — entered flag class using ``ValidationStatus``.
   
   Documentation for :ref:`Flag <root_api_command_flag>` — flag class with validation rules.
   
   Documentation for :ref:`PossibleValues <root_api_command_possible_values>` — types of allowed values.

-----

VALID
~~~~~

.. code-block:: python
   :linenos:

   ValidationStatus.VALID = 'VALID'

Indicates that the flag and its value **passed** validation.

Flags with this status comply with the rules defined in the ``possible_values`` of the corresponding ``Flag``. They can be safely used in application logic without additional checks.

**Conditions for receiving** ``VALID`` **status:**

*   Flag with ``PossibleValues.NEITHER`` passed without a value.
*   Flag with ``PossibleValues.ALL`` passed with any value or without one.
*   Flag value is in the list of allowed values.
*   Flag value matches the regular expression.

-----

INVALID
~~~~~~~

.. code-block:: python
   :linenos:

   ValidationStatus.INVALID = 'INVALID'

Indicates that the flag or its value **did not pass** validation.

Flags with this status violate the rules defined in the ``possible_values`` of the corresponding ``Flag``. They should be treated as erroneous.

**Conditions for receiving** ``INVALID`` **status:**

*   Flag with ``PossibleValues.NEITHER`` passed with a value.
*   Flag value is not in the list of allowed values.
*   Flag value does not match the regular expression.
*   Flag requires a value but was passed without one.

-----

UNDEFINED
~~~~~~~~~

.. code-block:: python
   :linenos:

   ValidationStatus.UNDEFINED = 'UNDEFINED'

Indicates that the entered flag was not registered in the command.

**Conditions for receiving** ``UNDEFINED`` **status:**

*   The entered flag is not found among those registered for this command.
