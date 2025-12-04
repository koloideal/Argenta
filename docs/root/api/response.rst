.. _root_api_response:

Response
========

``Response`` — это объект, который передаётся в обработчик команды. Он создаётся автоматически при обработке пользовательского ввода и содержит статус валидации, введённые флаги.


.. seealso::

   Документация по :ref:`InputFlags <root_api_command_input_flags>` — коллекция введённых флагов команды.

   Документация по :ref:`ResponseStatus <root_api_response_status>` — статусы валидации флагов команды.

   Документация по :ref:`InputFlag <root_api_command_input_flag>` — отдельный введённый флаг.

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

   __init__(
       self, status: ResponseStatus,
       input_flags: InputFlags = EMPTY_INPUT_FLAGS,
   )

Создаёт новый объект ответа.

* ``status``: Общий статус валидации флагов из перечисления ``ResponseStatus``.
* ``input_flags``: Коллекция введённых флагов (``InputFlags``). По умолчанию — пустая.

.. warning::
   Экземпляры этого класса не предназначены для прямого создания. Они автоматически формируются системой и передаются в обработчик команды в качестве первого обязательного аргумента.

**Атрибуты:**

.. py:attribute:: status
   :no-index:

   Общий статус валидации всех флагов команды (``ResponseStatus``). Указывает, были ли среди введённых флагов некорректные или незарегистрированные.

.. py:attribute:: input_flags
   :no-index:

   Коллекция всех флагов, переданных с командой (``InputFlags``). Содержит все обработанные флаги с их значениями и статусами валидации.

**Пример использования:**

.. literalinclude:: ../../code_snippets/response/snippet1.py
   :linenos:
   :language: python

-----

Работа с флагами
----------------

``Response`` предоставляет доступ к введённым флагам через атрибут ``input_flags``. Вы можете проверять их наличие, получать значения и статусы валидации.

**Пример работы с флагами:**

.. literalinclude:: ../../code_snippets/response/snippet6.py
   :linenos:
   :language: python

-----

.. _root_api_response_status:

ResponseStatus
--------------

``ResponseStatus`` — это перечисление, которое определяет общий статус валидации всех флагов команды. Используется в атрибуте ``status`` объекта ``Response``.

ALL_FLAGS_VALID
~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.ALL_FLAGS_VALID = 'ALL_FLAGS_VALID'

Все введённые флаги прошли валидацию. Нет ни некорректных, ни незарегистрированных флагов.

UNDEFINED_FLAGS
~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.UNDEFINED_FLAGS = 'UNDEFINED_FLAGS'

Среди введённых флагов есть незарегистрированные, но нет флагов с некорректными значениями.

INVALID_VALUE_FLAGS
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.INVALID_VALUE_FLAGS = 'INVALID_VALUE_FLAGS'

Среди введённых флагов есть флаги с некорректными значениями, но нет незарегистрированных.

UNDEFINED_AND_INVALID_FLAGS
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.UNDEFINED_AND_INVALID_FLAGS = 'UNDEFINED_AND_INVALID_FLAGS'

Среди введённых флагов есть как незарегистрированные, так и флаги с некорректными значениями.
