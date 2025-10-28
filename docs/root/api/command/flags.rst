.. _root_api_command_flags:

Flags
======

Объект ``Flags`` представляет собой коллекцию флагов команды в приложении ``Argenta``. Его основная задача — группировать и управлять набором флагов, зарегистрированных для конкретной команды. ``Flags`` служит контейнером, который позволяет удобно добавлять, извлекать и итерировать флаги, а также проверять их наличие.

``Flags`` наследуется от базового класса ``BaseFlags`` и специализируется для работы с объектами типа ``Flag``. Этот класс используется при создании команд с множественными флагами и предоставляет интерфейс для управления ими.

.. seealso::

   Документация по отдельным флагам (:ref:`Flag <root_api_command_flag>`, :ref:`InputFlag <root_api_command_input_flag>`)
   
   Документация по :ref:`InputFlags <root_api_command_input_flags>` — коллекции распаршенных флагов пользователя
   
   :ref:`Общая информация <root_flags>` о флагах и их использовании в приложении ``Argenta``

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

   __init__(self, flags: list[Flag] | None = None) -> None

Создает новую коллекцию флагов.

* ``flags`` : Необязательный список флагов типа ``Flag`` для инициализации коллекции. Если не указан, создается пустая коллекция.

**Атрибуты:**

.. py:attribute:: flags

   Список всех зарегистрированных флагов типа ``Flag``. Пустой список, если флаги не были переданы при инициализации.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flags_snippet.py
   :linenos:
   :language: python

-----

Методы
------

add_flag
~~~~~~~~

.. code-block:: python
   :linenos:

   add_flag(self, flag: Flag) -> None

Добавляет один флаг в коллекцию.

:param flag: Флаг типа ``Flag`` для добавления в коллекцию
:return: None

Метод добавляет переданный флаг в конец списка ``flags``. Используется для динамического расширения набора флагов после создания коллекции.

**Пример использования:**

.. code-block:: python
   :linenos:

   from argenta import Flags, ValueFlag, BooleanFlag

   # Создание коллекции
   flags = Flags()

   # Динамическое добавление флагов
   flags.add_flag(ValueFlag("config", help="Config file path"))
   flags.add_flag(BooleanFlag("debug", help="Debug mode"))
   flags.add_flag(ValueFlag("log-level", possible_values=["INFO", "DEBUG", "ERROR"]))

   print(len(flags.flags))  # 3

-----

add_flags
~~~~~~~~~

.. code-block:: python
   :linenos:

   add_flags(self, flags: list[Flag]) -> None

Добавляет список флагов в коллекцию.

:param flags: Список флагов типа ``Flag`` для добавления
:return: None

Метод расширяет текущую коллекцию, добавляя все флаги из переданного списка. Эффективен для пакетного добавления множества флагов.

**Пример использования:**

.. code-block:: python
   :linenos:

   from argenta import Flags, ValueFlag, BooleanFlag

   # Начальная коллекция
   flags = Flags([
       ValueFlag("host", default="localhost")
   ])

   # Дополнительные флаги
   additional_flags = [
       ValueFlag("port", default="8080"),
       ValueFlag("database", help="Database name"),
       BooleanFlag("ssl", help="Use SSL"),
       BooleanFlag("verbose", help="Verbose output")
   ]

   # Добавление списка флагов
   flags.add_flags(additional_flags)

   print(len(flags.flags))  # 5

-----

get_flag_by_name
~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_flag_by_name(self, name: str) -> Flag | None

Получает флаг по его имени.

:param name: Имя искомого флага
:return: Объект ``Flag`` с указанным именем или ``None``, если флаг не найден

Метод выполняет поиск по списку ``flags`` и возвращает первый флаг с соответствующим именем. Если флаг не найден, возвращается ``None``.

**Пример использования:**

.. code-block:: python
   :linenos:

   from argenta import Flags, ValueFlag, BooleanFlag

   flags = Flags([
       ValueFlag("host", default="localhost"),
       ValueFlag("port", default="8080"),
       BooleanFlag("verbose")
   ])

   # Получение флага по имени
   host_flag = flags.get_flag_by_name("host")
   if host_flag:
       print(f"Found flag: {host_flag.name}")
       print(f"Default value: {host_flag.default}")

   # Поиск несуществующего флага
   unknown_flag = flags.get_flag_by_name("nonexistent")
   if unknown_flag is None:
       print("Flag not found")

-----

Магические методы
-----------------

__iter__
~~~~~~~~

.. code-block:: python
   :linenos:

   __iter__(self) -> Iterator[Flag]

Делает коллекцию итерируемой, позволяя использовать её в циклах.

:return: Итератор по списку флагов

**Пример использования:**

.. code-block:: python
   :linenos:

   from argenta import Flags, ValueFlag, BooleanFlag

   flags = Flags([
       ValueFlag("host", default="localhost"),
       ValueFlag("port", default="8080"),
       BooleanFlag("verbose")
   ])

   # Итерация по всем флагам
   for flag in flags:
       print(f"Flag: {flag.name} (type: {type(flag).__name__})")

   # Использование в list comprehension
   flag_names = [flag.name for flag in flags]
   print(f"All flags: {flag_names}")

-----

__getitem__
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   __getitem__(self, flag_index: int) -> Flag

Позволяет получать флаги по индексу.

:param flag_index: Индекс флага в списке
:return: Флаг с указанным индексом

**Пример использования:**

.. code-block:: python
   :linenos:

   from argenta import Flags, ValueFlag

   flags = Flags([
       ValueFlag("first"),
       ValueFlag("second"),
       ValueFlag("third")
