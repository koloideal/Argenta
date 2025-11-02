.. _root_api_command_flag:

Flag
=====

``Flag`` — это сущность, описывающая флаг команды. Её основная задача — определить параметры флага, включая его имя, префикс и правила валидации. `Flag` используется при создании команд и предоставляет механизм для проверки значений, введённых пользователем.

.. seealso::

   Документация по :ref:`PossibleValues <root_api_command_possible_values>` — перечисление, определяющее типы допустимых значений.
   
   Документация по :ref:`InputFlag <root_api_command_input_flag>` — объект обработанного флага, введённого пользователем.
   
   :ref:`Общая информация <root_flags>` о флагах и их использовании в приложении ``Argenta``

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

   __init__(
       self, name: str, *,
       prefix: Literal["-", "--", "---"] = "--",
       possible_values: list[str] | Pattern[str] | PossibleValues = PossibleValues.ALL,
   ) -> None

Создаёт новый флаг для регистрации в команде.

* ``name``: Имя флага (обязательный параметр).
* ``prefix``: Префикс флага (``-``, ``--``, ``---``). По умолчанию ``--``.
* ``possible_values``: Правила валидации значения. Может быть списком строк, регулярным выражением или значением из `PossibleValues`. По умолчанию `PossibleValues.ALL`.

**Атрибуты:**

.. py:attribute:: name

   Имя флага в виде строки.

.. py:attribute:: prefix

   Префикс флага. Один из: ``"-"``, ``"--"``, ``"---"``.

.. py:attribute:: possible_values

   Определяет допустимые значения для флага:

*   Список строк: флаг принимает только значения из этого списка.
*   Регулярное выражение (`Pattern[str]`): значение проверяется на соответствие паттерну.
*   `PossibleValues.ALL`: флаг принимает любое значение.
*   `PossibleValues.NEITHER`: флаг не должен иметь значения.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flag/snippet.py
   :linenos:
   :language: python

-----

Свойства
--------

string_entity
~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   @property
   string_entity(self) -> str

Возвращает строковое представление флага в формате `prefix + name`.

:return: Строковое представление флага

Это свойство объединяет префикс и имя в единую строку, которая представляет флаг так, как он выглядел бы в командной строке.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flag/snippet3.py
   :linenos:
   :language: python

-----

Магические методы
-----------------

__str__
~~~~~~~

.. code-block:: python
   :linenos:

   __str__(self) -> str

Возвращает строковое представление флага (аналогично `string_entity`).

:return: Строковое представление флага

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flag/snippet4.py
   :linenos:
   :language: python

-----

__repr__
~~~~~~~~

.. code-block:: python
   :linenos:

   __repr__(self) -> str

Возвращает отладочное представление объекта.

:return: Строка в формате `Flag<prefix=..., name=...>`.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flag/snippet5.py
   :linenos:
   :language: python

-----

__eq__
~~~~~~

.. code-block:: python
   :linenos:

   __eq__(self, other: object) -> bool

Сравнивает два флага на равенство по их строковому представлению (`string_entity`).

:param other: Объект для сравнения
:return: ``True``, если флаги равны, иначе ``False``
:raises NotImplementedError: Если `other` не является экземпляром `Flag`.

Два флага считаются равными, если их `string_entity` идентичны.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flag/snippet6.py
   :linenos:
   :language: python

-----

.. _root_api_command_flag_predefined_flags:

PredefinedFlags
---------------

``argenta.command.PredefinedFlags``

Класс `PredefinedFlags` предоставляет набор готовых флагов для использования в приложениях без их ручного создания. Эти флаги покрывают наиболее распространённые сценарии и следуют общепринятым соглашениям.

Все предопределённые флаги являются атрибутами класса и представляют собой готовые экземпляры `Flag`.

-----

Доступные флаги
~~~~~~~~~~~~~~~

Информационные флаги


.. py:attribute:: PredefinedFlags.HELP

   Флаг для отображения справки: ``--help``
   
   * ``name``: ``"help"``
   * ``prefix``: ``"--"`` (по умолчанию)
   * ``possible_values``: ``PossibleValues.NEITHER``

.. py:attribute:: PredefinedFlags.SHORT_HELP

   Короткая версия флага справки: ``-H``
   
   * ``name``: ``"H"``
   * ``prefix``: ``"-"``
   * ``possible_values``: ``PossibleValues.NEITHER``

.. py:attribute:: PredefinedFlags.INFO

   Флаг для отображения информации: ``--info``
   
   * ``name``: ``"info"``
   * ``prefix``: ``"--"`` (по умолчанию)
   * ``possible_values``: ``PossibleValues.NEITHER``

.. py:attribute:: PredefinedFlags.SHORT_INFO

   Короткая версия флага информации: ``-I``
   
   * ``name``: ``"I"``
   * ``prefix``: ``"-"``
   * ``possible_values``: ``PossibleValues.NEITHER``

-----

Флаги выбора
~~~~~~~~~~~~

.. py:attribute:: PredefinedFlags.ALL

   Флаг для выбора всех элементов: ``--all``
   
   * ``name``: ``"all"``
   * ``prefix``: ``"--"``
   * ``possible_values``: ``PossibleValues.NEITHER``

.. py:attribute:: PredefinedFlags.SHORT_ALL

   Короткая версия флага выбора всех элементов: ``-A``
   
   * ``name``: ``"A"``
   * ``prefix``: ``"-"``
   * ``possible_values``: ``PossibleValues.NEITHER``

-----

Сетевые флаги
~~~~~~~~~~~~~

.. py:attribute:: PredefinedFlags.HOST

   Флаг для указания IP-адреса хоста: ``--host``
   
   * ``name``: ``"host"``
   * ``prefix``: ``"--"`` (по умолчанию)
   * ``possible_values``: Регулярное выражение для валидации IPv4: ``r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"``

.. py:attribute:: PredefinedFlags.SHORT_HOST

   Короткая версия флага хоста: ``-H``
   
   * ``name``: ``"H"``
   * ``prefix``: ``"-"``
   * ``possible_values``: Регулярное выражение для валидации IPv4: ``r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"``

.. py:attribute:: PredefinedFlags.PORT

   Флаг для указания порта: ``--port``
   
   * ``name``: ``"port"``
   * ``prefix``: ``"--"`` (по умолчанию)
   * ``possible_values``: Регулярное выражение для валидации порта: ``r"^\d{1,5}$"``

.. py:attribute:: PredefinedFlags.SHORT_PORT

   Короткая версия флага порта: ``-P``
   
   * ``name``: ``"P"``
   * ``prefix``: ``"-"``
   * ``possible_values``: Регулярное выражение для валидации порта: ``r"^\d{1,5}$"``

-----

**Пример использования:**

.. literalinclude:: ../../../code_snippets/flag/predefined_flags.py
   :linenos:
   :language: python
