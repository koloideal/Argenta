.. _root_api_command_input_flags:

InputFlags
==========

Объект ``InputFlags`` представляет собой коллекцию введённых флагов команды в приложении ``Argenta``. Его основная задача — группировать и управлять набором флагов, которые были введены пользователем вместе с командой. ``InputFlags`` служит контейнером, который позволяет удобно извлекать, итерировать и проверять наличие введённых флагов, а также работать с их значениями и статусами валидации.

``InputFlags`` наследуется от базового класса ``BaseFlags`` и специализируется для работы с объектами типа ``InputFlag``. Этот класс автоматически создаётся системой при парсинге пользовательского ввода и передаётся в обработчики команд через объект ``Response``.

.. seealso::

   Документация по отдельным флагам (:ref:`Flag <root_api_command_flag>`, :ref:`InputFlag <root_api_command_input_flag>`)
   
   Документация по :ref:`Flags <root_api_command_flags>` — коллекции зарегистрированных флагов команды
   
   Документация по :ref:`Response <root_api_response>` — объект ответа, содержащий ``InputFlags``
   
   :ref:`Общая информация <root_flags>` о флагах и их использовании в приложении ``Argenta``

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

   __init__(self, flags: list[InputFlag] | None = None) -> None

Создает новую коллекцию введённых флагов.

* ``flags`` : Необязательный список введённых флагов типа ``InputFlag`` для инициализации коллекции. Если не указан, создается пустая коллекция.

.. warning ::
   Экземпляры класса обычно не создаются напрямую. Они автоматически формируются системой при парсинге пользовательского ввода и доступны через атрибут ``input_flags`` объекта ``Response`` в обработчиках команд.

**Атрибуты:**

.. py:attribute:: flags

   Список всех введённых флагов типа ``InputFlag``. Пустой список, если флаги не были переданы при инициализации или пользователь не ввёл флагов с командой.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet1.py
   :linenos:
   :language: python

-----

Методы
------

get_flag_by_name
~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_flag_by_name(self, name: str) -> InputFlag | None

Получает введённый флаг по его имени.

:param name: Имя искомого флага (без префикса)
:return: Объект ``InputFlag`` с указанным именем или ``None``, если флаг не найден

Метод выполняет поиск по списку ``flags`` и возвращает первый флаг с соответствующим именем. Поиск происходит по атрибуту ``name`` объекта ``InputFlag``, сравнивая только имена флагов, без учёта префикса.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet2.py
   :linenos:
   :language: python

-----

add_flag
~~~~~~~~

.. code-block:: python
   :linenos:

   add_flag(self, flag: InputFlag) -> None

Добавляет один введённый флаг в коллекцию.

:param flag: Флаг типа ``InputFlag`` для добавления в коллекцию
:return: None

Метод добавляет переданный флаг в конец списка ``flags``. Используется для динамического расширения набора флагов после создания коллекции.

.. note::
   Этот метод используется редко, так как ``InputFlags`` обычно создаётся автоматически системой при парсинге пользовательского ввода. Однако он может быть полезен для тестирования или ручного создания коллекций флагов.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet3.py
   :linenos:
   :language: python

-----

add_flags
~~~~~~~~~

.. code-block:: python
   :linenos:

   add_flags(self, flags: list[InputFlag]) -> None

Добавляет список введённых флагов в коллекцию.

:param flags: Список флагов типа ``InputFlag`` для добавления
:return: None

Метод расширяет текущую коллекцию, добавляя все флаги из переданного списка. Эффективен для пакетного добавления множества флагов.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet4.py
   :linenos:
   :language: python

-----

Магические методы
-----------------

__iter__
~~~~~~~~

.. code-block:: python
   :linenos:

   __iter__(self) -> Iterator[InputFlag]

Делает коллекцию итерируемой, позволяя использовать её в циклах.

:return: Итератор по списку введённых флагов

Позволяет перебирать все введённые флаги команды, что особенно полезно для проверки статусов валидации или обработки всех флагов.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet5.py
   :linenos:
   :language: python

-----

__getitem__
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   __getitem__(self, flag_index: int) -> InputFlag

Позволяет получать введённые флаги по индексу.

:param flag_index: Индекс флага в списке
:return: Флаг с указанным индексом

Позволяет обращаться к флагам по их позиции в списке, что может быть полезно для обработки флагов в определённом порядке.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet6.py
   :linenos:
   :language: python

-----

__bool__
~~~~~~~~

.. code-block:: python
   :linenos:

   __bool__(self) -> bool

Определяет, содержит ли коллекция какие-либо флаги.

:return: ``True``, если в коллекции есть хотя бы один флаг, иначе ``False``

Позволяет проверять наличие флагов в команде, что удобно для условной логики.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet7.py
   :linenos:
   :language: python

-----

__eq__
~~~~~~

.. code-block:: python
   :linenos:

   __eq__(self, other: object) -> bool

Сравнивает две коллекции введённых флагов на равенство.

:param other: Объект для сравнения
:return: ``True``, если коллекции равны, иначе ``False``
:raises NotImplementedError: Если ``other`` не является экземпляром ``InputFlags``

Две коллекции считаются равными, если они содержат одинаковое количество флагов и все соответствующие флаги равны (сравнение происходит по правилам ``InputFlag.__eq__``, то есть по имени).

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet8.py
   :linenos:
   :language: python

-----

__contains__
~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   __contains__(self, ingressable_item: object) -> bool

Проверяет, содержится ли указанный введённый флаг в коллекции.

:param ingressable_item: Объект ``InputFlag`` для проверки
:return: ``True``, если флаг найден в коллекции, иначе ``False``
:raises TypeError: Если ``ingressable_item`` не является экземпляром ``InputFlag``

Позволяет использовать оператор ``in`` для проверки наличия флага в коллекции.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet9.py
   :linenos:
   :language: python

-----

Практические примеры
--------------------

Обработка всех флагов с проверкой статусов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Пример демонстрирует, как итерироваться по всем введённым флагам и проверять их статусы валидации:

.. literalinclude:: ../../../code_snippets/input_flags/snippet10.py
   :linenos:
   :language: python
