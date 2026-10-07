.. _root_api_command_flags:

Flags
=====

``Flags`` is a collection of command flags. Its main purpose is to group and manage the set of flags registered for a specific command. ``Flags`` serves as a container that allows convenient addition, retrieval, iteration of flags, and checking their presence.

.. seealso::

   Documentation for individual flags (:ref:`Flag <root_api_command_flag>`, :ref:`InputFlag <root_api_command_input_flag>`)
   
   Documentation for :ref:`InputFlags <root_api_command_input_flags>` — a collection of processed flags entered by the user.
   
   :ref:`General information <root_flags>` about flags and their usage in the ``Argenta`` application

-----

Initialization
--------------

.. code-block:: python
   :linenos:

   __init__(self, flags: list[Flag] | None = None) -> None

Creates a new flag collection.

* ``flags``: Optional list of flags of type ``Flag`` for initializing the collection. If not specified, an empty collection is created.

**Attributes:**

.. py:attribute:: flags
   :no-index:

   List of all registered flags of type ``Flag``. 

**Usage example:**

.. literalinclude:: ../../../code_snippets/flags/snippet.py
   :linenos:
   :language: python

-----

Methods
-------

add_flag
~~~~~~~~

.. code-block:: python
   :linenos:

   add_flag(self, flag: Flag) -> None

Adds a flag to the collection.

:param flag: Flag of type ``Flag`` to add.
:return: None.

Used for dynamically extending the set of flags.

**Usage example:**

.. literalinclude:: ../../../code_snippets/flags/snippet2.py
   :linenos:
   :language: python

-----

add_flags
~~~~~~~~~

.. code-block:: python
   :linenos:

   add_flags(self, flags: list[Flag]) -> None

Adds a list of flags to the collection.

:param flags: List of flags of type ``Flag`` to add.
:return: None.

The method extends the collection by adding all flags from the provided list. Efficient for batch addition.

**Usage example:**

.. literalinclude:: ../../../code_snippets/flags/snippet3.py
   :linenos:
   :language: python

-----

get_flag_by_name
~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_flag_by_name(self, name: str) -> Flag | None

Returns a flag by name.

:param name: Name of the flag to search for.
:return: ``Flag`` object or ``None`` if the flag is not found.

The method returns a flag with the corresponding name. If the flag is not found, ``None`` is returned.

**Usage example:**

.. literalinclude:: ../../../code_snippets/flags/snippet4.py
   :linenos:
   :language: python
