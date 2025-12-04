.. _root_api_app_index:

App
===

Объект ``App`` — это ядро вашего консольного приложения. Он отвечает за конфигурацию, управление жизненным циклом, обработку команд и взаимодействие с пользователем, координируя работу всех компонентов: роутеров, обработчиков и системных сообщений.

------

Инициализация
-------------

.. code-block:: python
   :linenos:

    AVAILABLE_DIVIDING_LINES: TypeAlias = StaticDividingLine | DynamicDividingLine
    DEFAULT_DIVIDING_LINE: StaticDividingLine = StaticDividingLine()
    
    DEFAULT_PRINT_FUNC: Printer = Console().print
    DEFAULT_AUTOCOMPLETER: AutoCompleter = AutoCompleter()
    DEFAULT_EXIT_COMMAND: Command = Command("Q", description="Exit command")

.. code-block:: python
    :linenos:
    
    def __init__(self, *, prompt: str = "What do you want to do?\n\n", 
                initial_message: str = "Argenta\n", 
                farewell_message: str = "\nSee you\n", 
                exit_command: Command = DEFAULT_EXIT_COMMAND, 
                system_router_title: str | None = "System points:", 
                ignore_command_register: bool = True, 
                dividing_line: AVAILABLE_DIVIDING_LINES = DEFAULT_DIVIDING_LINE, 
                repeat_command_groups_printing: bool = True, 
                override_system_messages: bool = False, 
                autocompleter: AutoCompleter = DEFAULT_AUTOCOMPLETER, 
                print_func: Printer = DEFAULT_PRINT_FUNC) -> None

Создаёт и настраивает экземпляр приложения.

    * ``prompt``: Приглашение к вводу, отображаемое перед каждой командой.
    * ``initial_message``: Сообщение, выводимое при запуске приложения.
    * ``farewell_message``: Сообщение, выводимое при выходе из приложения.
    * ``exit_command``: Команда, которая маркируется как триггер для выхода из приложения.
    * ``system_router_title``: Заголовок для системного роутера (содержит команду выхода).
    * ``ignore_command_register``: Если ``True``, регистр вводимых команд игнорируется при поиске обработчика.
    * ``dividing_line``: Тип разделительной линии (``StaticDividingLine`` или ``DynamicDividingLine``).
    * ``repeat_command_groups_printing``: Если ``True``, список доступных команд выводится перед каждым вводом.
    * ``override_system_messages``: Если ``True``, стандартное форматирование (цвета, ASCII-арт) отключается.
    * ``autocompleter``: Экземпляр класса :ref:`AutoCompleter <root_api_app_autocompleter>`, отвечающий за автодополнение команд.
    * ``print_func``: Функция для вывода всех системных сообщений (по умолчанию ``rich.Console().print``).

-----
    
Основные методы
---------------

- .. py:method:: include_router(self, router: Router) -> None

    Регистрирует роутер в приложении. Все команды из этого роутера становятся доступными для вызова.
    
    :param router: Экземпляр ``Router`` для регистрации.

- .. py:method:: include_routers(self, *routers: Router) -> None

    Регистрирует несколько роутеров одновременно.
    
    :param routers: Последовательность экземпляров ``Router`` для регистрации.

- .. py:method:: add_message_on_startup(self, message: str) -> None

    Добавляет текстовое сообщение, которое выводится при запуске приложения после ``initial_message``.

    :param message: Строка с сообщением.

    .. seealso::
       Для вывода стандартных сообщений можно использовать готовые шаблоны из :ref:`PredefinedMessages <root_api_predefined_messages>`.
    
-----

Методы установки обработчиков
-------------------------------

``App`` позволяет настраивать реакцию на различные события, такие как ошибки ввода или неизвестные команды.

.. hint::
   Подробнее об исключениях и их обработке в соответствующем :ref:`разделе документации <root_error_handling>`.
   
-----

.. py:method:: set_description_message_pattern(self, handler: Callable[[str, str], str]) -> None

   Устанавливает шаблон для форматирования описания команды.
   
   Обработчик принимает триггер команды (``str``) и её описание (``str``).
   
------

.. py:method:: set_incorrect_input_syntax_handler(self, handler: Callable[[str], None]) -> None

   Устанавливает обработчик при некорректном введённом синтаксисе флагов.
   
   Обработчик принимает строку, введённую пользователем.
   
------

.. py:method:: set_repeated_input_flags_handler(self, handler: Callable[[str], None]) -> None

   Устанавливает обработчик при повторяющихся флагах в введённой команде.
   
   Обработчик принимает строку, введённую пользователем.
   
------

.. py:method:: set_unknown_command_handler(self, handler: Callable[[InputCommand], None]) -> None

   Устанавливает обработчик при вводе неизвестной команды.
   
   Обработчик принимает объект ``InputCommand`` - объект введённой команды.
   
-----

.. py:method:: set_empty_command_handler(self, handler: Callable[[], None]) -> None

   Устанавливает обработчик при вводе пустой строки.
   
   Обработчик не принимает аргументов.
   
-----

.. py:method:: set_exit_command_handler(self, handler: Callable[[Response], None]) -> None

   Переопределяет стандартное поведение при вызове команды выхода.
   
   Обработчик принимает объект ``Response``.

.. toctree::
    :hidden:

    autocompleter
    dividing_lines

-----

.. _root_api_predefined_messages:

PredefinedMessages
------------------

``PredefinedMessages`` — это контейнер, содержащий набор готовых к использованию сообщений. Они отформатированы с использованием синтаксиса ``rich`` и предназначены для вывода стандартной информации, такой как подсказки по использованию.

Рекомендуется использовать их при старте приложения.

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

      orchestrator.start_polling(app)

   if __name__ == "__main__":
      main()
    

.. py:class:: PredefinedMessages
   :no-index:

   .. py:attribute:: USAGE

      Строка: ``[b dim]Usage[/b dim]: [i]<command> <[green]flags[/green]>[/i]``

      Отображается как: ``Usage: <command> <flags>``

   .. py:attribute:: HELP

      Строка: ``[b dim]Help[/b dim]: [i]<command>[/i] [b red]--help[/b red]``

      Отображается как: ``Help: <command> --help``

   .. py:attribute:: AUTOCOMPLETE

      Строка: ``[b dim]Autocomplete[/b dim]: [i]<part>[/i] [bold]<tab>``

      Отображается как: ``Autocomplete: <part> <tab>``
