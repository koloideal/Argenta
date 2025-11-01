.. _root_api_response:

Response
========

Объект ``Response`` представляет собой сущность ответа пользовательского ввода, передаваемого в обработчик команды. Он создаётся автоматически при парсинге пользовательского ввода и содержит информацию о статусе валидации флагов, введённые флаги, а также предоставляет механизм для передачи данных между обработчиками команд через глобальное хранилище данных.

``Response`` наследуется от ``DataBridge``, который предоставляет методы для работы с глобальным хранилищем данных, позволяющим обмениваться данными между различными обработчиками команд в контексте приложения.

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

Создаёт новый объект ответа на пользовательский ввод.

* ``status`` : Статус валидации флагов команды из перечисления ``ResponseStatus``
* ``input_flags`` : Коллекция введённых флагов команды. По умолчанию используется пустая коллекция ``EMPTY_INPUT_FLAGS``

.. warning ::
   Экземпляры класса не предназначены для их прямого создания. Они автоматически создаются системой при обработке пользовательского ввода и передаются в обработчики команд в качестве обязательного первого аргумента.

**Атрибуты:**

.. py:attribute:: status

   Статус валидации всех флагов команды типа ``ResponseStatus``. Указывает, были ли среди введённых флагов невалидные или незарегистрированные.

.. py:attribute:: input_flags

   Коллекция всех флагов, переданных с командой, типа ``InputFlags``. Содержит все распарсенные флаги команды с их значениями и статусами валидации.

**Пример использования:**

.. literalinclude:: ../../code_snippets/response/snippet1.py
   :linenos:
   :language: python

-----

Методы DataBridge

``Response`` наследует от ``DataBridge`` методы для работы с глобальным хранилищем данных, которое позволяет передавать информацию между различными обработчиками команд в рамках одного сеанса работы приложения.

update_data
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   @classmethod
   update_data(cls, data: dict[str, Any]) -> None

Обновляет глобальное хранилище данных, добавляя или обновляя значения из переданного словаря.

:param data: Словарь с данными для обновления хранилища
:return: None

Метод объединяет переданные данные с существующими данными в хранилище. Если ключ уже существует, его значение будет обновлено.

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

Получает все данные из глобального хранилища.

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

Очищает все данные из глобального хранилища.

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

Удаляет конкретный ключ и его значение из глобального хранилища данных.

:param key: Ключ, который необходимо удалить из хранилища
:return: None
:raises KeyError: Если указанный ключ не существует в хранилище

**Пример использования:**

.. literalinclude:: ../../code_snippets/response/snippet5.py
   :linenos:
   :language: python

-----

Работа с флагами
----------------

``Response`` предоставляет доступ к введённым флагам команды через атрибут ``input_flags``. Вы можете проверять наличие флагов, получать их значения и статусы валидации.

**Пример работы с флагами:**

.. literalinclude:: ../../code_snippets/response/snippet6.py
   :linenos:
   :language: python

-----

.. _root_api_response_status:

ResponseStatus
--------------

Enum ``ResponseStatus`` представляет собой перечисление, определяющее общий статус валидации всех флагов команды. Используется в атрибуте ``status`` объекта ``Response`` для информирования о результате проверки всех введённых флагов.

Значения enum
~~~~~~~~~~~~~

ALL_FLAGS_VALID
~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.ALL_FLAGS_VALID = 'ALL_FLAGS_VALID'

Указывает, что все введённые флаги команды прошли валидацию успешно. Нет ни невалидных, ни незарегистрированных флагов.

UNDEFINED_FLAGS
~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.UNDEFINED_FLAGS = 'UNDEFINED_FLAGS'

Указывает, что среди введённых флагов присутствуют незарегистрированные флаги, но нет флагов с невалидными значениями.

INVALID_VALUE_FLAGS
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.INVALID_VALUE_FLAGS = 'INVALID_VALUE_FLAGS'

Указывает, что среди введённых флагов присутствуют флаги с невалидными значениями, но нет незарегистрированных флагов.

UNDEFINED_AND_INVALID_FLAGS
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   ResponseStatus.UNDEFINED_AND_INVALID_FLAGS = 'UNDEFINED_AND_INVALID_FLAGS'

Указывает, что среди введённых флагов одновременно присутствуют и незарегистрированные флаги, и флаги с невалидными значениями.
