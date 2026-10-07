.. _root_api_app_index:

App
===

The ``App`` object is the implementations of your console application. It handles configuration, lifecycle management, command processing, and user interaction, coordinating the work of all components: routers, handlers, and system messages.

------

Initialization
--------------

.. code-block:: python
    :linenos:
    
    def __init__(
        self,
        *,
        prompt: str = ">>> ",
        initial_message: str = "Argenta",
        farewell_message: str = "See you",
        exit_command: Command = Command("q", description="Exit command"),
        system_router_title: str = "System points:",
        dividing_line: StaticDividingLine | DynamicDividingLine | None = None,
        repeat_command_groups_printing: bool = False,
        override_system_messages: bool = False,
        autocompleter: AutoCompleter | None = None,
        printer: Printer = Console().print,
    ) -> None:

Creates and configures an application instance.

    * ``prompt``: Input prompt displayed before each command.
    * ``initial_message``: Message displayed when the application starts.
    * ``farewell_message``: Message displayed when exiting the application.
    * ``exit_command``: Command that is marked as a trigger for exiting the application.
    * ``system_router_title``: Title for the system router (contains the exit command).
    * ``dividing_line``: Type of dividing line (``StaticDividingLine`` or ``DynamicDividingLine``).
    * ``repeat_command_groups_printing``: If ``True``, the list of available commands is displayed before each input.
    * ``override_system_messages``: If ``True``, standard formatting (colors, ASCII art) is disabled.
    * ``autocompleter``: Instance of the :ref:`AutoCompleter <root_api_app_autocompleter>` class responsible for command autocompletion.
    * ``print_func``: Function for outputting all system messages (defaults to ``rich.Console().print``).

-----

.. note::
    In applications on Argenta, the case of the entered commands is not important, checking for the  existence and routing of commands is performed based on triggers reduced to lowercase.
    
Main Methods
------------

- .. py:method:: include_router(self, router: Router) -> None

    Registers a router in the application. All commands from this router become available for invocation.
    
    :param router: ``Router`` instance to register.

- .. py:method:: include_routers(self, *routers: Router) -> None

    Registers multiple routers simultaneously.
    
    :param routers: Sequence of ``Router`` instances to register.

- .. py:method:: add_message_on_startup(self, message: str) -> None

    Adds a text message that is displayed when the application starts after ``initial_message``.

    :param message: String with the message.

    .. seealso::
       For outputting standard messages, you can use ready-made templates from :ref:`PredefinedMessages <root_api_predefined_messages>`.
    
-----

Handler Setup Methods
---------------------

``App`` allows you to configure responses to various events, such as input errors or unknown commands.

.. hint::
   For more details on exceptions and their handling, see the corresponding :ref:`documentation section <root_error_handling>`.
   
-----

.. py:method:: set_description_message_pattern(self, handler: Callable[[str, str], str]) -> None

   Sets the template for formatting command descriptions.
   
   The handler accepts the command trigger (``str``) and its description (``str``).
   
------

.. py:method:: set_incorrect_input_syntax_handler(self, handler: Callable[[str], None]) -> None

   Sets the handler for incorrect flag syntax input.
   
   The handler accepts the string entered by the user.
   
------

.. py:method:: set_repeated_input_flags_handler(self, handler: Callable[[str], None]) -> None

   Sets the handler for duplicate flags in the entered command.
   
   The handler accepts the string entered by the user.
   
------

.. py:method:: set_unknown_command_handler(self, handler: Callable[[InputCommand], None]) -> None

   Sets the handler for entering an unknown command.
   
   The handler accepts an ``InputCommand`` object - the entered command object.
   
-----

.. py:method:: set_empty_command_handler(self, handler: Callable[[], None]) -> None

   Sets the handler for entering an empty string.
   
   The handler accepts no arguments.
   
-----

.. py:method:: set_exit_command_handler(self, handler: Callable[[Response], None]) -> None

   Overrides the default behavior when the exit command is invoked.
   
   The handler accepts a ``Response`` object.

.. toctree::
    :hidden:

    autocompleter
    dividing_lines

-----

.. _root_api_predefined_messages:

PredefinedMessages
------------------

``PredefinedMessages`` is a container containing a set of ready-to-use messages. They are formatted using ``rich`` syntax and are intended for displaying standard information, such as usage hints.

It is recommended to use them when starting the application.

.. code-block:: python
   :linenos:

   from argenta import App, Orchestrator
   from argenta.app import PredefinedMessages

   app: App = App()
   orchestrator: Orchestrator = Orchestrator()

   def main():
      app.add_message_on_startup(PredefinedMessages.USAGE)
      app.add_message_on_startup(PredefinedMessages.AUTOCOMPLETE)
      app.add_message_on_startup(PredefinedMessages.HELP)

      orchestrator.run_repl(app)

   if __name__ == "__main__":
      main()
    

.. py:class:: PredefinedMessages
   :no-index:

   .. py:attribute:: USAGE

      String: ``[b dim]Usage[/b dim]: [i]<command> <[green]flags[/green]>[/i]``

      Displayed as: ``Usage: <command> <flags>``

   .. py:attribute:: HELP

      String: ``[b dim]Help[/b dim]: [i]<command>[/i] [b red]--help[/b red]``

      Displayed as: ``Help: <command> --help``

   .. py:attribute:: AUTOCOMPLETE

      String: ``[b dim]Autocomplete[/b dim]: [i]<part>[/i] [bold]<tab>``

      Displayed as: ``Autocomplete: <part> <tab>``
