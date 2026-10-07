.. _root_flags:

Input Command Flags
===================

Flags are special parameters that users can add to commands to control their behavior. 

Why Flags Are Needed in Commands
--------------------------------

Controlling Command Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main purpose of flags is to provide a way to change the command's logic without reworking it. A command can operate in several modes: standard, verbose, debug, or simplified. Flags switch these modes on user demand, keeping the implementations functionality unchanged.

Optionality and Convenience
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Flags solve the problem of mandatory parameters. If all command parameters are made required, it makes the command difficult to use. Flags allow you to specify only the values needed in a specific situation, while others use default values.

When Flags Might Be Needed
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Switching Operation Modes**
  A command deploys an application normally, but a mode without actual deployment (dry-run) is needed for verification. The ``--dry-run`` flag will switch the mode.

**Adjusting Verbosity Level**
  When debugging or analyzing, more information about the command execution process is required. The ``--verbose`` or ``--debug`` flags provide detailed output.

**Managing Error Behavior**
  By default, a command may abort on the first error. The ``--force`` flag allows continuing execution, skipping non-critical errors.

**Output Formatting**
  A command outputs data as text, but in some scenarios JSON or CSV is needed. The ``--format=json`` flag will switch the output format.

**Combining Options**
  Often a combination of several changes is needed: verbose output, dry-run mode, and JSON format. Multiple flags solve this task simultaneously.

Practical Significance
~~~~~~~~~~~~~~~~~~~~~~

Flags make commands more predictable and controllable. Users can start with simple usage and then add flags as needed. This is especially important when automating tasks in scripts, where interface flexibility is critical.

Flags also facilitate command integration into various systems, as additional behavior is achieved without changing the command structure, only through passing optional parameters.

-----

Flag Syntax
-----------

The general syntax looks like this:

.. code-block:: py

   <command_name> <flag_prefix: Literal['-', '--', '---']><flag_name> <flag_value: Optional>

A flag consists of a prefix (``-``, ``--``, or ``---``), a name, and optionally a value, which is specified with a space.

**Examples:**

.. code-block:: shell

   greet --name John
   deploy --verbose
   backup -f --compress

-----

Working with Flags in Handlers
------------------------------

To get the flag value in a handler, use the ``response.input_flags`` object of type :ref:`InputFlags <root_api_command_input_flags>`.

**Example with a flag that has a value:**

.. literalinclude:: ../code_snippets/flags/greet_handler.py
   :language: python
   :linenos:

**Example with a toggle flag:**

.. literalinclude:: ../code_snippets/flags/deploy_handler.py
   :language: python
   :linenos:

.. seealso::
   For more details on working with the ``InputFlags`` object, see the :ref:`InputFlags <root_api_command_input_flags>` section.

-----

Two Types of Flags
------------------

Flags come in two main types:

1. **Flags with values** — accept a parameter after the flag name (for example, ``--name John``, ``--port 8080``)
2. **Toggle flags** — do not accept values, their presence itself is a signal (for example, ``--verbose``, ``--force``)

``Argenta`` allows registering and entering flags of both types in any sequence for a single command.

.. note::
    Validation errors do not throw exceptions. Instead, each :ref:`InputFlag <root_api_command_input_flag>` object has a ``status`` attribute that can be used to determine if validation was successful. A detailed description of the API for creating flags is in the :ref:`Flag <root_api_command_flag>` section.

When registering a flag, you can set validation rules for its value. By default, any value is considered valid. Validation can be configured in several ways:

-----

Flags vs Arguments
------------------

In the context of Argenta, flags and arguments belong to different levels of interaction with the application.

**Arguments** are parameters passed when launching the application. They define the global configuration throughout its operation (for example, database address, logging level).

.. seealso:: API and more detailed description in the :ref:`ArgParser <root_api_orchestrator_argparser>` and :ref:`Arguments <root_api_orchestrator_arguments>` sections.

**Flags** are command operation parameters available within an interactive session when entering each new command. They allow modifying the behavior of a specific command without restarting the application.

.. seealso:: API and more detailed description in the :ref:`Flag <root_api_command_flag>` section.

-----

Key Differences
~~~~~~~~~~~~~~~

**Lifetime**
  Arguments are passed once at startup and remain in effect for the entire application runtime. Flags are local and exist only within the execution of a command.

**Mutability**
  To change arguments, the application must be restarted. Flags can be changed with each command input.

**Purpose**
  Arguments control the global configuration of the application. Flags control the behavior of individual commands.

-----
  
Practical Examples
~~~~~~~~~~~~~~~~~~

Arguments at application startup:

- Database connection address
- Operation mode (production, development, testing)
- Logging level

Flags in an interactive session:

- ``deploy --verbose --dry-run`` — for the deployment command
- ``backup --compress --encrypted`` — for the backup command
- ``test --parallel --coverage`` — for the testing command
