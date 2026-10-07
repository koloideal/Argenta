.. _root_api_command_index:

Command
=======

``Command`` is the basic unit of functionality in an application. Each command links a handler to a trigger, which when entered will invoke it for processing.

``Command`` encapsulates all information about a command: its trigger (keyword for invocation), description, set of flags, and set of aliases.

-----

Initialization
--------------

.. code-block:: python
   :linenos:

   __init__(self, trigger: str, *,
            description: str | None = None,
            flags: Flag | Flags = DEFAULT_WITHOUT_FLAGS,
            aliases: set[str] = DEFAULT_WITHOUT_ALIASES) -> None

Creates a new command for registration in a router.

* ``trigger``: String trigger that the user enters to invoke the command. Serves as the primary identifier.
* ``description``: Optional description explaining the command's purpose. Displayed in help.
* ``flags``: Set of flags for configuring behavior. Can be a single ``Flag`` object or a ``Flags`` collection.
* ``aliases``: Set of string aliases for the main trigger.

**Attributes:**

.. py:attribute:: trigger

   The main command trigger. Used for its identification when processing user input.

.. py:attribute:: description

   Text description of the command. If not provided, the default value is used.

.. py:attribute:: registered_flags

   A ``Flags`` object containing all registered flags. If a ``Flag`` was passed, it is automatically converted from a single flag to a collection during initialization.

.. py:attribute:: aliases

   Set of string aliases. Empty if no aliases are defined.

**Usage example:**

.. literalinclude:: ../../../code_snippets/command/snippet.py
   :linenos:
   
.. seealso ::
   More about flags: :ref:`Flags <root_api_command_flags>` and :ref:`Command flags <root_flags>`.

-----

Command Registration
--------------------

Commands are passed as an argument to the ``@router.command()`` decorator.

**Basic example:**

.. literalinclude:: ../../../code_snippets/command/snippet2.py
   :linenos:

**Commands with flags:**

.. literalinclude:: ../../../code_snippets/command/snippet3.py
   :linenos:

-----

Working with Aliases
--------------------

Aliases allow invoking the same handler with different triggers while preserving the command's flags and description.

**Example with aliases:**

.. literalinclude:: ../../../code_snippets/command/snippet5.py
   :linenos:

Now the user can invoke the command in any of the following ways:

.. code-block:: bash

   shutdown
   poweroff
   halt
   stop

All these variants will invoke the same handler ``handle_shutdown``.

-----
    
.. _root_api_command_input_command:

InputCommand
------------

``InputCommand`` represents a processed command entered by the user. This internal class is created automatically when processing user input. Direct work with it is possible when creating a custom handler for unknown commands.

.. seealso ::
   For more details on custom exception handlers, see :ref:`here <root_error_handling_unknown_command>`.

**Attributes:**

.. py:attribute:: trigger
   :no-index:

   String trigger entered by the user.

.. py:attribute:: input_flags
   :no-index:

   An ``InputFlags`` object containing all entered and parsed flags.

.. toctree ::
    :hidden:
    
    flag
    possible_values
    input_flag
    validation_status
    flags 
    input_flags
