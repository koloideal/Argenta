.. _root_api_command_input_flag:

InputFlag
=========

Объект ``InputFlag`` представляет собой сущность флага введённой команды. Он создаётся в результате парсинга пользовательского ввода и содержит информацию о распознанном флаге, включая его имя, префикс, введённое значение и статус валидации.

.. seealso::

   Документация по :ref:`Flag <root_api_command_flag>` — сущность флага, регистрируемого для последующей обработки.

   Документация по :ref:`ValidationStatus <root_api_command_validation_status>` — статусы валидации флагов.

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

   __init__(
       self, name: str, *,
       prefix: Literal['-', '--', '---'] = '--',
       input_value: str | None,
       status: ValidationStatus | None
   )

Создаёт новый объект введённого флага.

* ``name`` : Имя введённого флага (обязательный параметр)
* ``prefix`` : Префикс флага. По умолчанию ``"--"``. Возможные значения: ``"-"``, ``"--"``, ``"---"``
* ``input_value`` : Значение введённого флага. Может быть ``None`` если флаг не принимает значения
* ``status`` : Статус валидации флага из перечисления ``ValidationStatus``

.. warning ::
   Экземпляры класса не предназначены для их прямого создания, они содержаться в контейнере :ref:`Response <root_api_response>`

**Атрибуты:**

.. py:attribute:: name
   :no-index:

   Имя введённого флага в виде строки.

.. py:attribute:: prefix
   :no-index:

   Префикс флага. Один из: ``"-"``, ``"--"``, ``"---"``.

.. py:attribute:: input_value

   Значение, переданное с флагом в командной строке. Может быть ``None`` для флагов без значений.

.. py:attribute:: status

   Статус валидации флага. Один из: ``ValidationStatus.VALID``, ``ValidationStatus.INVALID``, ``ValidationStatus.UNDEFINED``.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flag/snippet1.py
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

Возвращает строковое представление флага в формате ``prefix + name``.

:return: Строковое представление флага

Это свойство объединяет префикс и имя флага в единую строку, которая представляет, как флаг был введён в командной строке.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flag/snippet2.py
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

Возвращает строковое представление введённого флага вместе с его значением.

:return: Строка в формате ``флаг значение``

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flag/snippet3.py
   :linenos:
   :language: python

-----

__repr__
~~~~~~~~

.. code-block:: python
   :linenos:

   __repr__(self) -> str

Возвращает отладочное представление объекта введённого флага.

:return: Строка в формате ``InputFlag<prefix=..., name=..., value=..., status=...>``

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flag/snippet4.py
   :linenos:
   :language: python

-----

__eq__
~~~~~~

.. code-block:: python
   :linenos:

   __eq__(self, other: object) -> bool

Сравнивает два введённых флага на равенство по их имени.

:param other: Объект для сравнения
:return: ``True``, если имена флагов совпадают, иначе ``False``
:raises NotImplementedError: Если ``other`` не является экземпляром ``InputFlag``

Два введённых флага считаются равными, если их имена идентичны.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flag/snippet5.py
   :linenos:
   :language: python
