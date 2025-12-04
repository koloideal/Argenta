.. _root_api_orchestrator_arguments:

Arguments
=========

Модуль ``Arguments`` предоставляет классы для работы с аргументами командной строки. Они позволяют настраивать поведение приложения в момент его запуска, передавая различные параметры конфигурации.

Аргументы регистрируются в ``ArgParser`` и после обработки становятся доступными в объекте ``ArgSpace``.

-----

ValueArgument
-------------

Класс для аргументов, требующих передачи значения.

.. py:class:: ValueArgument(BaseArgument)
    :no-index:

.. code-block:: python
   :linenos:

   __init__(self, name: str, *,
            prefix: Literal["-", "--", "---"] = "--",
            help: str = "Help message for the value argument",
            possible_values: list[str] | None = None,
            default: str | None = None,
            is_required: bool = False,
            is_deprecated: bool = False) -> None

Создаёт аргумент командной строки, требующий значения.

:param name: Имя аргумента
:param prefix: Префикс (по умолчанию ``--``)
:param help: Сообщение для справки (``--help``)
:param possible_values: Список допустимых значений 
:param default: Значение по умолчанию, если аргумент не передан
:param is_required: Если ``True``, аргумент становится обязательным. Если не передать при запуске, приложение не запустится
:param is_deprecated: Если ``True``, помечает аргумент как устаревший. Если передать при запуске, будет выведено предупреждение в консоль

**Пример использования:**

.. literalinclude:: ../../../code_snippets/arguments/snippet.py
   :language: python
   :linenos:

**Запуск приложения:**

.. code-block:: bash

   python app.py --host 127.0.0.1
   python app.py --host 127.0.0.1 --config custom.yaml --log-level DEBUG

-----

BooleanArgument
---------------

Класс для булевых аргументов, не требующих значения. Их наличие при запуске устанавливает значение в **True**, отсутствие — в **False**.

.. py:class:: BooleanArgument(BaseArgument)
    :no-index:

.. code-block:: python
   :linenos:

   __init__(self, name: str, *,
            prefix: Literal["-", "--", "---"] = "--",
            help: str = "Help message for the boolean argument",
            is_deprecated: bool = False) -> None

Создаёт булев аргумент командной строки без значения.

:param name: Имя аргумента
:param prefix: Префикс (по умолчанию ``--``)
:param help: Сообщение для справки (``--help``)
:param is_deprecated: Если ``True``, помечает аргумент как устаревший

**Пример использования:**

.. literalinclude:: ../../../code_snippets/arguments/snippet2.py
   :language: python
   :linenos:

**Запуск приложения:**

.. code-block:: bash

   python app.py --verbose
   python app.py --debug --no-cache
   python app.py  # without arguments

-----

.. _root_api_orchestrator_arguments_inputargument:

InputArgument
-------------

.. seealso::
   ``InputArgument`` напрямую связан с контейнером ``ArgSpace`` и является его наполнителем. Подробнее о нём см. :ref:`здесь <root_api_orchestrator_argspace>`.

Представляет собой обработанный аргумент командной строки. Этот класс используется внутри ``ArgSpace`` для хранения значений, полученных после парсинга.

.. py:class:: InputArgument
    :no-index:

.. code-block:: python
   :linenos:

   __init__(self, name: str,
            value: str | Literal[True],
            founder_class: type[BaseArgument]) -> None

Создаёт экземпляр обработанного входного аргумента.

:param name: Имя аргумента
:param value: Значение аргумента. Для ``BooleanArgument`` — **True**, если аргумент передан, и **False**, если нет; для ``ValueArgument`` — введённая строка 
:param founder_class: Класс-родитель, из которого был создан аргумент (``BooleanArgument`` или ``ValueArgument``)

**Атрибуты:**

.. py:attribute:: name
   :no-index:

   Имя аргумента, указанное при создании ``ValueArgument`` или ``BooleanArgument``.

.. py:attribute:: value

   Значение аргумента. Тип зависит от исходного класса:

   * Для ``BooleanArgument``: **True**, если аргумент был передан
   * Для ``ValueArgument``: строка с переданным значением или значением по умолчанию

.. py:attribute:: founder_class

   Ссылка на класс-родитель. Используется для определения типа и фильтрации.
