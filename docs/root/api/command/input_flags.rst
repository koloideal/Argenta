.. _root_api_command_input_flags:

InputFlags
==========

``InputFlags`` is a collection of flags entered by the user. Its main purpose is to group and manage the set of flags passed with a command. ``InputFlags`` serves as a container that allows convenient retrieval, iteration, and checking of flag presence, as well as working with their values and validation statuses.

.. seealso::

   Documentation for individual flags (:ref:`Flag <root_api_command_flag>`, :ref:`InputFlag <root_api_command_input_flag>`)

   Documentation for :ref:`InputFlags <root_api_command_input_flags>` — a collection of processed flags entered by the user.

   Documentation for :ref:`Response <root_api_response>` — response object containing ``InputFlags``

   :ref:`General information <root_flags>` about flags and their usage in the ``Argenta`` application

-----

Initialization
--------------

.. code-block:: python
   :linenos:

   __init__(self, flags: list[InputFlag] | None = None) -> None

Creates a new collection of entered flags.

* ``flags``: Optional list of flags of type ``InputFlag`` for initializing the collection. If not specified, an empty collection is created.

.. warning ::
   Instances of this class are usually not created directly. They are automatically formed by the system when processing user input and are accessible through the ``input_flags`` attribute of the ``Response`` object.

**Attributes:**

.. py:attribute:: flags
   :no-index:

   List of all entered flags of type ``InputFlag``. Empty if flags were not passed during initialization or the user did not enter them with the command.

**Usage example:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet1.py
   :linenos:
   :language: python

-----

Methods
-------

get_flag_by_name
~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_flag_by_name(self, name: str) -> InputFlag | None

Returns a flag by name.

:param name: Name of the flag to search for (without prefix).
:return: ``InputFlag`` object or ``None`` if the flag is not found.

The method returns the first flag with the corresponding name (ignoring the prefix).

**Usage example:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet2.py
   :linenos:
   :language: python

-----

add_flag
~~~~~~~~

.. code-block:: python
   :linenos:

   add_flag(self, flag: InputFlag) -> None

Adds an entered flag to the collection.

:param flag: Flag of type ``InputFlag`` to add.
:return: None.

The method adds a flag to the end of the ``flags`` list. Used for dynamically extending the collection.

.. note::
   This method is rarely used, as `InputFlags` is usually created automatically. However, it can be useful for testing or manual collection creation.

**Usage example:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet3.py
   :linenos:
   :language: python

-----

add_flags
~~~~~~~~~

.. code-block:: python
   :linenos:

   add_flags(self, flags: list[InputFlag]) -> None

Adds a list of entered flags to the collection.

:param flags: List of flags of type ``InputFlag`` to add.
:return: None.

The method extends the collection by adding all flags from the provided list. Efficient for batch addition.

**Usage example:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet4.py
   :linenos:
   :language: python

-----

Practical Examples
------------------

Processing All Flags with Status Checking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Usage example:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet10.py
   :linenos:
   :language: python
