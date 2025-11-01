.. _root_api_command_input_flag:

InputFlag
=========

Объект `InputFlag` представляет собой флаг, введённый пользователем. Он создаётся в результате обработки пользовательского ввода и содержит информацию о распознанном флаге: его имя, префикс, значение и статус валидации.

.. seealso::

   Документация по :ref:`Flag <root_api_command_flag>` — класс для регистрации флага.

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

* ``name``: Имя введённого флага.
* ``prefix``: Префикс флага (``-``, ``--``, ``---``). По умолчанию ``--``.
* ``input_value``: Значение, переданное с флагом. Может быть `None`.
* ``status``: Статус валидации из перечисления `ValidationStatus`.

.. warning ::
   Экземпляры этого класса не предназначены для прямого создания. Они содержатся в объекте :ref:`Response <root_api_response>`.

**Атрибуты:**

.. py:attribute:: name
   :no-index:

   Имя введённого флага.

.. py:attribute:: prefix
   :no-index:

   Префикс флага: ``-``, ``--`` или ``---``.

.. py:attribute:: input_value

   Значение, переданное с флагом. Может быть `None` для флагов без значений.

.. py:attribute:: status
   :no-index:

   Статус валидации флага: `ValidationStatus.VALID`, `ValidationStatus.INVALID` или `ValidationStatus.UNDEFINED`.

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

Возвращает строковое представление флага в формате `prefix + name`.

:return: Строковое представление флага

Это свойство объединяет префикс и имя в строку, представляющую флаг так, как он был введён в командной строке.

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

Возвращает строковое представление флага вместе с его значением.

:return: Строка в формате `флаг значение`.

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

Возвращает отладочное представление объекта.

:return: Строка в формате `InputFlag<prefix=..., name=..., value=..., status=...>`.

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

Сравнивает два введённых флага на равенство по имени.

:param other: Объект для сравнения.
:return: `True`, если имена флагов совпадают, иначе `False`.
:raises NotImplementedError: Если `other` не является экземпляром `InputFlag`.

Два введённых флага считаются равными, если их имена совпадают.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flag/snippet5.py
   :linenos:
   :language: python
