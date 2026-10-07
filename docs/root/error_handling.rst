.. _root_error_handling:

Error Handling
==============

``Argenta`` throws exceptions in edge cases related to user input. By default, they are handled by system handlers, but you can override them. This is done using ``App`` instance setters of the form ``.set_*_handler()``. More details about each of them are described :ref:`below <possible_errors>`.

.. note::
    No exception goes unhandled, as a default handler is provided for each case. Therefore, overriding is optional.

**Usage example:**

.. literalinclude:: ../code_snippets/error_handling/snippet.py
    :language: python
    :linenos:


.. _possible_errors:

Possible Exceptions and Non-Standard Behavior
---------------------------------------------

``UnprocessedInputFlagException``: Incorrect Flag Syntax
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This exception is thrown when the parser cannot process a command due to incorrect syntax. Most often this is related to an error in flag syntax. You can read more about them in the :ref:`Flags <root_flags>` section.

The default handler outputs to the console:

.. code-block::  shell

    Incorrect flag syntax: <raw input command>

To override, use the ``.set_incorrect_input_syntax_handler()`` setter. It accepts a handler with the signature ``Callable[[str], None]``, where the only argument is a string with the unprocessed command.

**Usage example:**

.. literalinclude:: ../code_snippets/error_handling/snippet2.py
   :language: python
   :linenos:

---------------

``RepeatedInputFlagsException``: Repeated Flags in Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The exception is thrown if the user entered a command with repeated flags. Two flags (:ref:`InputFlag <root_api_command_input_flag>`) are considered the same if their names match. More about flags and their syntax in the :ref:`Flags <root_flags>` section.

.. note::
    Equality comparison for registered flags (``Flag``) works differently, see :ref:`Flag <root_flags>` for details.

The default handler outputs to the console:

.. code-block::  shell

    Repeated input flags: <raw input command>

To override, use the ``.set_repeated_input_flags_handler()`` setter. It accepts a handler with the signature ``Callable[[str], None]``, where the only argument is a string with the unprocessed command.

**Usage example:**

.. literalinclude:: ../code_snippets/error_handling/snippet3.py
   :language: python
   :linenos:

---------------

``EmptyInputCommandException``: Empty Command Entered
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The exception is thrown if the user entered an empty string or a string consisting only of whitespace characters (``\n``, ``\t``, space, etc.).

The default handler outputs to the console:

.. code-block::  shell

    Empty input command

To override, use the ``.set_empty_command_handler()`` setter. It accepts a handler with the signature ``Callable[[], None]`` (no arguments).

**Usage example:**

.. literalinclude:: ../code_snippets/error_handling/snippet4.py
    :language: python
    :linenos:

---------------

.. _root_error_handling_unknown_command:

Handling Unknown Commands
~~~~~~~~~~~~~~~~~~~~~~~~~

This behavior is triggered when the user enters a command that is not registered in any of the routers and is not an alias for an existing command.

The default handler outputs to the console:

.. code-block::  shell

    Unknown command: <trigger of the input command>

To override, use the ``.set_unknown_command_handler()`` setter. It accepts a handler with the signature ``Callable[[InputCommand], None]``, where the argument is an :ref:`InputCommand <root_api_command_input_command>` object.

**Usage example:**

.. literalinclude:: ../code_snippets/error_handling/snippet5.py
    :language: python
    :linenos:

---------------

Exiting the Application
~~~~~~~~~~~~~~~~~~~~~~~

This behavior is triggered when the user enters a command marked as an exit command.

The default handler outputs text to the console and terminates the application:

.. code-block::  shell

    See you

To override, use the ``.set_exit_command_handler()`` setter. It accepts a handler with the signature ``Callable[[Response], None]``, where the argument is a :ref:`Response <root_api_response>` object.

**Usage example:**

.. literalinclude:: ../code_snippets/error_handling/snippet6.py
    :language: python
    :linenos:
