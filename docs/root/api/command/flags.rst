.. _root_api_command_flags:

Flags
======

`Flags` — это коллекция флагов команды. Её основная задача — группировать и управлять набором флагов, зарегистрированных для конкретной команды. `Flags` служит контейнером, который позволяет удобно добавлять, извлекать, итерировать флаги и проверять их наличие.

`Flags` наследуется от базового класса `BaseFlags` и специализируется на работе с объектами типа `Flag`. Этот класс используется при создании команд с несколькими флагами и предоставляет интерфейс для управления ими.

.. seealso::

   Документация по отдельным флагам (:ref:`Flag <root_api_command_flag>`, :ref:`InputFlag <root_api_command_input_flag>`)
   
   Документация по :ref:`InputFlags <root_api_command_input_flags>` — коллекция обработанных флагов, введённых пользователем.
   
   :ref:`Общая информация <root_flags>` о флагах и их использовании в приложении ``Argenta``

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

   __init__(self, flags: list[Flag] | None = None) -> None

Создаёт новую коллекцию флагов.

* ``flags``: Необязательный список флагов типа `Flag` для инициализации коллекции. Если не указан, создаётся пустая коллекция.

**Атрибуты:**

.. py:attribute:: flags
   :no-index:

   Список всех зарегистрированных флагов типа `Flag`. Пуст, если флаги не были переданы при инициализации.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flags/snippet.py
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

Добавляет флаг в коллекцию.

:param flag: Флаг типа `Flag` для добавления.
:return: None.

Метод добавляет флаг в конец списка `flags`. Используется для динамического расширения набора флагов.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flags/snippet2.py
   :linenos:
   :language: python

-----

add_flags
~~~~~~~~~

.. code-block:: python
   :linenos:

   add_flags(self, flags: list[Flag]) -> None

Добавляет в коллекцию список флагов.

:param flags: Список флагов типа `Flag` для добавления.
:return: None.

Метод расширяет коллекцию, добавляя в неё все флаги из переданного списка. Эффективен для пакетного добавления.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flags/snippet3.py
   :linenos:
   :language: python

-----

get_flag_by_name
~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_flag_by_name(self, name: str) -> Flag | None

Возвращает флаг по имени.

:param name: Имя искомого флага.
:return: Объект `Flag` или `None`, если флаг не найден.

Метод выполняет поиск по списку `flags` и возвращает первый флаг с соответствующим именем. Если флаг не найден, возвращается `None`.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flags/snippet4.py
   :linenos:
   :language: python

-----

Магические методы
-----------------

__iter__
~~~~~~~~

.. code-block:: python
   :linenos:

   __iter__(self) -> Iterator[Flag]

Делает коллекцию итерируемой для использования в циклах.

:return: Итератор по списку флагов.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flags/snippet5.py
   :linenos:
   :language: python

-----

__getitem__
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   __getitem__(self, flag_index: int) -> Flag

Позволяет получать флаг по индексу.

:param flag_index: Индекс флага в списке.
:return: Флаг по указанному индексу.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flags/snippet6.py
   :linenos:
   :language: python
