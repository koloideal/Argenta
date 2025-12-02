.. _root_api_command_input_flags:

InputFlags
==========

``InputFlags`` — это коллекция флагов, введённых пользователем. Её основная задача — группировать и управлять набором флагов, переданных вместе с командой. ``InputFlags`` служит контейнером, который позволяет удобно извлекать, итерировать и проверять наличие флагов, а также работать с их значениями и статусами валидации.

.. seealso::

   Документация по отдельным флагам (:ref:`Flag <root_api_command_flag>`, :ref:`InputFlag <root_api_command_input_flag>`)

   Документация по :ref:`InputFlags <root_api_command_input_flags>` — коллекция обработанных флагов, введённых пользователем.

   Документация по :ref:`Response <root_api_response>` — объект ответа, содержащий ``InputFlags``

   :ref:`Общая информация <root_flags>` о флагах и их использовании в приложении ``Argenta``

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

   __init__(self, flags: list[InputFlag] | None = None) -> None

Создаёт новую коллекцию введённых флагов.

* ``flags``: Необязательный список флагов типа ``InputFlag`` для инициализации коллекции. Если не указан, создаётся пустая коллекция.

.. warning ::
   Экземпляры этого класса обычно не создаются напрямую. Они автоматически формируются системой при обработке пользовательского ввода и доступны через атрибут ``input_flags`` объекта ``Response``.

**Атрибуты:**

.. py:attribute:: flags
   :no-index:

   Список всех введённых флагов типа ``InputFlag``. Пуст, если флаги не были переданы при инициализации или пользователь не ввёл их с командой.

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

Возвращает флаг по имени.

:param name: Имя искомого флага (без префикса).
:return: Объект ``InputFlag`` или ``None``, если флаг не найден.

Метод возвращает первый флаг с соответствующим именем (без учёта префикса).

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

Добавляет введённый флаг в коллекцию.

:param flag: Флаг типа ``InputFlag`` для добавления.
:return: None.

Метод добавляет флаг в конец списка ``flags``. Используется для динамического расширения коллекции.

.. note::
   Этот метод используется редко, так как `InputFlags` обычно создаётся автоматически. Однако он может быть полезен для тестирования или ручного создания коллекций.

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

Добавляет в коллекцию список введённых флагов.

:param flags: Список флагов типа ``InputFlag`` для добавления.
:return: None.

Метод расширяет коллекцию, добавляя в неё все флаги из переданного списка. Эффективен для пакетного добавления.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet4.py
   :linenos:
   :language: python

-----

Практические примеры
--------------------

Обработка всех флагов с проверкой статусов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Пример использования:**

.. literalinclude:: ../../../code_snippets/input_flags/snippet10.py
   :linenos:
   :language: python
