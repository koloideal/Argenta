.. _root_api_app_index:

App
===

Объект ``App`` является центральной сущностью библиотеки ``Argenta``. Он выступает в роли ядра вашего консольного приложения, отвечая за его конфигурацию, управление жизненным циклом, обработку команд и взаимодействие с пользователем. ``App`` координирует работу всех остальных компонентов, таких как роутеры, обработчики команд и системные сообщения.

------

Инициализация
-------------

.. code:: rust

    AVAILABLE_DIVIDING_LINES: TypeAlias = StaticDividingLine | DynamicDividingLine
    DEFAULT_DIVIDING_LINE: StaticDividingLine = StaticDividingLine()
    
    DEFAULT_PRINT_FUNC: Printer = Console().print
    DEFAULT_AUTOCOMPLETER: AutoCompleter = AutoCompleter()
    DEFAULT_EXIT_COMMAND: Command = Command("Q", description="Exit command")

.. code:: python
    
    def __init__(self, *, prompt: str = "What do you want to do?\n\n", 
                initial_message: str = "Argenta\n", 
                farewell_message: str = "\nSee you\n", 
                exit_command: Command = DEFAULT_EXIT_COMMAND, 
                system_router_title: str | None = "System points:", 
                ignore_command_register: bool = True, 
                dividing_line: AVAILABLE_DIVIDING_LINES = DEFAULT_DIVIDING_LINE, 
                repeat_command_groups: bool = True, 
                override_system_messages: bool = False, 
                autocompleter: AutoCompleter = DEFAULT_AUTOCOMPLETER, 
                print_func: Printer = DEFAULT_PRINT_FUNC) -> None

Создает и настраивает экземпляр приложения `Argenta`.

    * ``prompt``:  Строка-приглашение, которая отображается перед вводом каждой команды. По умолчанию: **"What do you want to do?\\n\\n"**.
    * ``initial_message``: Приветственное сообщение, которое выводится при запуске приложения.
    * ``farewell_message``: Прощальное сообщение при завершении работы приложения.
    * ``exit_command``: Сущность команды, которая будет маркирована как команда для выхода из приложения.
    * ``system_router_title``: Заголовок для системного роутера, который содержит команду выхода и другие системные команды.
    * ``ignore_command_register``: Если **True** (по умолчанию), регистр введенных команд будет игнорироваться при поиске обработчика.
    * ``dividing_line``: Объект, управляющий стилем разделительной линии. Может быть **StaticDividingLine** или **DynamicDividingLine**.
    * ``repeat_command_groups``: Если **True** (по умолчанию), описание доступных команд будет выводиться перед каждым вводом.
    * ``override_system_messages``: Если **True** (по умолчанию), стандартное форматирование системных сообщений (цвета, ASCII-арт) будет отключено.
    * ``autocompleter``: Объект, отвечающий за логику автодополнения команд.
    * ``print_func``: Функция, используемая для вывода всех системных сообщений. По умолчанию используется ``rich.console.Console().print``.

Основные методы
---------------

.. py:method:: include_router(self, router: Router) -> None

   Регистрирует один `Router` в приложении. Все команды, определенные в этом роутере, становятся доступными для вызова.

   :param router: Объект роутера, который нужно зарегистрировать.

.. py:method:: include_routers(self, *routers: Router) -> None

   Регистрирует несколько роутеров одновременно. Является удобной оберткой над `include_router`.

   :param routers: Последовательность объектов `Router` для регистрации.

.. py:method:: add_message_on_startup(self, message: str) -> None

   Добавляет дополнительное текстовое сообщение, которое будет выведено на экран при запуске приложения, сразу после `initial_message`.

   :param message: Строка с сообщением.

Методы установки обработчиков
-------------------------------

`App` позволяет гибко настраивать реакцию на различные события, такие как ошибки ввода или ввод неизвестной команды.

.. py:method:: set_description_message_pattern(self, handler: DescriptionMessageGenerator) -> None

   Устанавливает пользовательский шаблон для форматирования строки, описывающей доступную команду (триггер + описание).

.. py:method:: set_incorrect_input_syntax_handler(self, handler: NonStandardBehaviorHandler[str]) -> None

   Устанавливает обработчик, который вызывается при некорректном синтаксисе флагов в введенной команде.

.. py:method:: set_repeated_input_flags_handler(self, handler: NonStandardBehaviorHandler[str]) -> None

   Устанавливает обработчик для ситуации, когда пользователь вводит один и тот же флаг несколько раз.

.. py:method:: set_unknown_command_handler(self, handler: NonStandardBehaviorHandler[InputCommand]) -> None

   Устанавливает обработчик, который срабатывает, если введенная команда не была найдена ни в одном из зарегистрированных роутеров.

.. py:method:: set_empty_command_handler(self, handler: EmptyCommandHandler) -> None

   Устанавливает обработчик для случая, когда пользователь отправляет пустую строку вместо команды.

.. py:method:: set_exit_command_handler(self, handler: NonStandardBehaviorHandler[Response]) -> None

   Позволяет переопределить стандартное поведение при вызове команды выхода. По умолчанию просто выводится `farewell_message`.

.. toctree::
    :hidden:

    autocompleter
    dividing_lines
