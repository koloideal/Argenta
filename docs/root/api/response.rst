.. _root_api_response:

Response
========

`Response` — это объект, который передаётся в обработчик команды. Он создаётся автоматически при обработке пользовательского ввода и содержит статус валидации, введённые флаги, а также предоставляет механизм для обмена данными между обработчиками.

`Response` наследует от `DataBridge` методы для работы с глобальным хранилищем, что позволяет обмениваться данными между обработчиками в рамках одной сессии.

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
       self,
       status: ResponseStatus,
       input_flags: InputFlags = EMPTY_INPUT_FLAGS,
   )

Создаёт новый объект ответа.

* ``status``: Общий статус валидации флагов из перечисления `ResponseStatus`.
* ``input_flags``: Коллекция введённых флагов (`InputFlags`). По умолчанию — пустая.

.. warning ::
   Экземпляры этого класса не предназначены для прямого создания. Они автоматически формируются системой и передаются в обработчик команды в качестве первого обязательного аргумента.

**Атрибуты:**

.. py:attribute:: status
   :no-index:

   Общий статус валидации всех флагов команды (`ResponseStatus`). Указывает, были ли среди введённых флагов некорректные или незарегистрированные.

.. py:attribute:: input_flags
   :no-index:

   Коллекция всех флагов, переданных с командой (`InputFlags`). Содержит все обработанные флаги с их значениями и статусами валидации.

**Пример использования:**

.. literalinclude:: ../../code_snippets/response/snippet1.py
   :linenos:
   :language: python

-----

Методы DataBridge

`Response` наследует от `DataBridge` методы для работы с глобальным хранилищем, которое позволяет обмениваться данными между обработчиками в рамках одной сессии.

update_data
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   @classmethod
   update_data(cls, data: dict[str, Any]) -> None

Обновляет глобальное хранилище, добавляя или изменяя значения из переданного словаря.

:param data: Словарь с данными для обновления хранилища
:return: None

Метод объединяет переданный словарь с данными в хранилище. Если ключ уже существует, его значение обновляется.

**Пример использования:**

.. literalinclude:: ../../code_snippets/response/snippet2.py
   :linenos:
   :language: python

-----

get_data
~~~~~~~~

.. code-block:: python
   :linenos:

   @classmethod
   get_data(cls) -> dict[str, Any]

Возвращает все данные из глобального хранилища.

:return: Словарь со всеми данными из хранилища

**Пример использования:**

.. literalinclude:: ../../code_snippets/response/snippet3.py
   :linenos:
   :language: python

-----

clear_data
~~~~~~~~~~

.. code-block:: python
   :linenos:

   @classmethod
   clear_data(cls) -> None

Очищает глобальное хранилище.

:return: None

**Пример использования:**

.. literalinclude:: ../../code_snippets/response/snippet4.py
   :linenos:
   :language: python

-----

delete_from_data
~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   @classmethod
   delete_from_data(cls, key: str) -> None

Удаляет ключ и его значение из глобального хранилища.

:param key: Ключ, который необходимо удалить из хранилища
:return: None
:raises KeyError: Если ключ не найден в хранилище.

**Пример использования:**

.. literalinclude:: ../../code_snippets/response/snippet5.py
   :linenos:
   :language: python

-----

Работа с флагами
----------------

`Response` предоставляет доступ к введённым флагам через атрибут `input_flags`. Вы можете проверять их наличие, получать значения и статусы валидации.

**Пример работы с флагами:**

.. literalinclude:: ../../code_snippets/response/snippet6.py
   :linenos:
   :language: python

-----

.. _root_api_response_status:

ResponseStatus
--------------

`ResponseStatus` — это перечисление (`Enum`), которое определяет общий статус валидации всех флагов команды. Используется в атрибуте `status` объекта `Response`.

Значения enum
~~~~~~~~~~~~~

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
