.. _root_api_response:

Response
========

``Response`` is an object that is passed to the command handler. It is created automatically when processing user input and contains validation status and entered flags.


.. seealso::

   Documentation for :ref:`InputFlags <root_api_command_input_flags>` — collection of entered command flags.

   Documentation for :ref:`ResponseStatus <root_api_response_status>` — command flag validation statuses.

   Documentation for :ref:`InputFlag <root_api_command_input_flag>` — individual entered flag.

-----

Initialization
--------------

.. code-block:: python
   :linenos:

   __init__(
       self, status: ResponseStatus,
       input_flags: InputFlags = EMPTY_INPUT_FLAGS,
   )

Creates a new response object.

* ``status``: Overall flag validation status from the ``ResponseStatus`` enumeration.
* ``input_flags``: Collection of entered flags (``InputFlags``). Empty by default.

.. warning::
   Instances of this class are not intended for direct creation. They are automatically formed by the system and passed to the command handler as the first required argument.

**Attributes:**

.. py:attribute:: status
   :no-index:

   Overall validation status of all command flags (``ResponseStatus``). Indicates whether there were any incorrect or unregistered flags among the entered ones.

.. py:attribute:: input_flags
   :no-index:

   Collection of all flags passed with the command (``InputFlags``). Contains all processed flags with their values and validation statuses.

**Usage example:**

.. literalinclude:: ../../code_snippets/response/snippet1.py
   :linenos:
   :language: python

-----

Working with Flags
------------------

``Response`` provides access to entered flags through the ``input_flags`` attribute. You can check their presence, get values, and validation statuses.

**Example of working with flags:**

.. literalinclude:: ../../code_snippets/response/snippet6.py
   :linenos:
   :language: python

-----

.. _root_api_response_status:

ResponseStatus
--------------

``ResponseStatus`` is an enumeration that defines the overall validation status of all command flags. Used in the ``status`` attribute of the ``Response`` object.

ALL_FLAGS_VALID
~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.ALL_FLAGS_VALID = 'ALL_FLAGS_VALID'

All entered flags passed validation. There are no incorrect or unregistered flags.

UNDEFINED_FLAGS
~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.UNDEFINED_FLAGS = 'UNDEFINED_FLAGS'

Among the entered flags, there are unregistered ones, but no flags with incorrect values.

INVALID_VALUE_FLAGS
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.INVALID_VALUE_FLAGS = 'INVALID_VALUE_FLAGS'

Among the entered flags, there are flags with incorrect values, but no unregistered ones.

UNDEFINED_AND_INVALID_FLAGS
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.UNDEFINED_AND_INVALID_FLAGS = 'UNDEFINED_AND_INVALID_FLAGS'

Among the entered flags, there are both unregistered flags and flags with incorrect values.
