.. _root_api_router:

Router
======

``Router`` is the main building block for organizing logic in an application. Its purpose is to group related commands and their handlers. Each router represents a logical container for a specific set of functions.

For example, in a user management application, one router can handle authentication (``login``, ``logout``), while another handles profile operations (``profile-show``, ``profile-edit``).

-----

Initialization
--------------

.. code-block:: python
   :linenos:

      __init__(self, title: str | None = None, 
               disable_redirect_stdout: bool = False) -> None

Creates a new router instance.

* ``title``: Optional title for the command group. Displayed in the list of available commands to help users navigate.
* ``disable_redirect_stdout``: If ``True``, disables ``stdout`` capture for all commands in this router. This is necessary for interactive commands (e.g., with ``input()``). When capture is disabled, a static separator line is automatically used. See :ref:`Overriding standard output <root_redirect_stdout>` for more details.

-----

Command Registration
--------------------

The ``@command`` decorator is used to register a command and bind a handler to it.

.. py:method:: @command(self, command: Command | str)

   Decorator for registering a function as a command handler.

   :param command: A ``Command`` instance describing the trigger, flags, and command description. Can be a string that will become the trigger (without the ability to configure flags and description).

   **Usage example:**

   .. literalinclude:: ../../code_snippets/router/snippet.py
      :linenos:
      :language: python
      
-----

System Router
-------------

``Argenta`` comes with a built-in system router that is automatically connected to every application.

.. py:data:: system_router
   :no-index:

   A predefined ``Router`` instance with basic system commands (by default, the exit command). Has the title **"System points:"**, which can be overridden in ``App``.

   You can add your own commands to this router. To do this, use the ``.system_router`` attribute of the created ``Orchestrator`` instance and use its ``@command`` decorator.

-----   
   
Possible Exceptions
-------------------

The following exceptions may occur when registering commands and flags in ``Router``:

.. py:exception:: TriggerContainSpacesException

   Raised if the command trigger in ``Command`` contains spaces. Triggers must be a single word.

   **Incorrect:** ``Command("add user")``
   
   **Correct:** ``Command("add-user")``

.. py:exception:: RepeatedFlagNameException

   Raised if duplicate names were used when defining flags for a command. Flag names within a single command must be unique.

   **Example that raises an exception:**

   .. code-block:: python
      :linenos:

      Command("send", flags=[
          Flag("recipient"),
          Flag("recipient")  # Duplicate!
      ])

.. py:exception:: RequiredArgumentNotPassedException

   Raised if the command handler does not accept the required ``Response`` argument.

.. py:exception:: RepeatedTriggerNameException

   Raised if duplicate triggers were used when registering commands in the router. Each command must have a unique trigger within a single router.

   **Example that raises an exception:**

   .. code-block:: python
      :linenos:

      router = Router()
      
      @router.command(Command("start"))
      def start_handler(response: Response) -> None:
          pass
      
      @router.command(Command("start"))  # Duplicate trigger!
      def another_start_handler(response: Response) -> None:
          pass

.. py:exception:: RepeatedAliasNameException

   Raised if duplicate aliases were used when registering commands. Aliases must be unique within the entire router.

   **Example that raises an exception:**

   .. code-block:: python
      :linenos:

      router = Router()
      
      @router.command(Command("start", aliases={"s", "run"}))
      def start_handler(response: Response) -> None:
          pass
      
      @router.command(Command("begin", aliases={"s"}))  # Duplicate alias "s"!
      def begin_handler(response: Response) -> None:
          pass

