.. _root_api_router:

Router
=============

``Router`` — это основной строительный блок для организации логики в приложении. Его задача — группировать связанные команды и их обработчики. Каждый роутер представляет собой логический контейнер для определённого набора функций.

Например, в приложении для управления пользователями один роутер может отвечать за аутентификацию (``login``, ``logout``), а другой — за операции с профилем (``profile-show``, ``profile-edit``).

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

      __init__(self, title: str | None = None, 
               disable_redirect_stdout: bool = False) -> None

Создаёт новый экземпляр роутера.

* ``title``: Необязательный заголовок для группы команд. Отображается в списке доступных команд, помогая пользователю ориентироваться.
* ``disable_redirect_stdout``: Если ``True``, отключает перехват ``stdout`` для всех команд этого роутера. Это необходимо для интерактивных команд (например, с ``input()``). При отключении перехвата автоматически используется статическая разделительная линия. Подробнее см. в разделе :ref:`Переопределение стандартного вывода <root_redirect_stdout>`.

-----

Регистрация команд
------------------

Для регистрации команды и привязки к ней обработчика используется декоратор ``@command``.

.. py:method:: @command(self, command: Command | str)

   Декоратор для регистрации функции как обработчика команды.

   :param command: Экземпляр ``Command``, описывающий триггер, флаги и описание команды. Может быть строкой, которая станет триггером (без возможности настройки флагов и описания).

   **Пример использования:**

   .. literalinclude:: ../../code_snippets/router/snippet.py
      :linenos:
      :language: python
      
-----

Системный роутер
-----------------------------

``Argenta`` поставляется со встроенным системным роутером, который автоматически подключается к каждому приложению.

.. py:data:: system_router
   :no-index:

   Предопределённый экземпляр ``Router`` с базовыми системными командами (по умолчанию — команда выхода). Имеет заголовок **«System points:»**, который можно переопределить в ``App``.

   Вы можете добавлять свои команды в этот роутер. Для этого используйте атрибут ``.system_router`` у созданного экхемпляра ``Orchestrator`` и используйте его декоратор ``@command``.

-----   
   
Возможные исключения
--------------------

При регистрации команд и флагов в ``Router`` могут возникнуть следующие исключения:

.. py:exception:: TriggerContainSpacesException

   Выбрасывается, если триггер команды в ``Command`` содержит пробелы. Триггеры должны быть одним словом.

   **Неправильно:** ``Command("add user")``
   
   **Правильно:** ``Command("add-user")``

.. py:exception:: RepeatedFlagNameException

   Возникает, если при определении флагов для команды были использованы дублирующиеся имена. Имена флагов в рамках одной команды должны быть уникальны.

   **Пример, вызывающий исключение:**

   .. code-block:: python
      :linenos:

      Command("send", flags=[
          Flag("recipient"),
          Flag("recipient")  # Duplicate!
      ])

.. py:exception:: RequiredArgumentNotPassedException

   Возникает, если обработчик команды не принимает обязательный аргумент ``Response``.

.. py:exception:: RepeatedTriggerNameException

   Возникает, если при регистрации команд в роутере были использованы дублирующиеся триггеры. Каждая команда должна иметь уникальный триггер в рамках приложения.

   **Пример, вызывающий исключение:**

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

   Возникает, если при регистрации команд были использованы дублирующиеся алиасы. Алиасы должны быть уникальны в рамках всего приложения.

   **Пример, вызывающий исключение:**

   .. code-block:: python
      :linenos:

      router = Router()
      
      @router.command(Command("start", aliases={"s", "run"}))
      def start_handler(response: Response) -> None:
          pass
      
      @router.command(Command("begin", aliases={"s"}))  # Duplicate alias "s"!
      def begin_handler(response: Response) -> None:
          pass

