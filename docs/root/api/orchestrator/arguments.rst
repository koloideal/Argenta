.. _root_api_orchestrator_arguments:

Arguments
=========

Модуль ``Arguments`` предоставляет классы для работы с аргументами командной строки. Они позволяют настраивать поведение приложения в момент его запуска, передавая различные параметры конфигурации.

Аргументы регистрируются в `ArgParser` и после обработки становятся доступными в объекте `ArgSpace`.

-----

ValueArgument
-------------

Класс для аргументов, требующих передачи значения. Используется для параметров конфигурации, которым необходимо указать значение при запуске.

.. py:class:: ValueArgument(BaseArgument)

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
:param possible_values: Список допустимых значений (передаётся в `choices` `ArgumentParser`)
:param default: Значение по умолчанию, если аргумент не передан
:param is_required: Если ``True``, аргумент становится обязательным
:param is_deprecated: Если ``True``, помечает аргумент как устаревший

**Пример использования:**

.. code-block:: python
   :linenos:

   from argenta import ArgParser, ValueArgument

   # Создание аргументов
   config_arg = ValueArgument(
       "config",
       help="Path to configuration file",
       default="config.yaml"
   )

   log_level_arg = ValueArgument(
       "log-level",
       help="Logging level",
       possible_values=["DEBUG", "INFO", "WARNING", "ERROR"],
       default="INFO"
   )

   host_arg = ValueArgument(
       "host",
       help="Server host address",
       is_required=True
   )

   # Регистрация в ArgParser
   parser = ArgParser(
       processed_args=[config_arg, log_level_arg, host_arg],
       name="MyApp",
       description="My application with CLI arguments"
   )

**Запуск приложения:**

.. code-block:: bash

   python app.py --host 127.0.0.1
   python app.py --host 127.0.0.1 --config custom.yaml --log-level DEBUG

-----

BooleanArgument
---------------

Класс для булевых аргументов, не требующих значения. Их наличие при запуске устанавливает значение в `True`, отсутствие — в `False`.

.. py:class:: BooleanArgument(BaseArgument)

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

.. code-block:: python
   :linenos:

   from argenta import ArgParser, BooleanArgument

   # Создание булевых аргументов
   verbose_arg = BooleanArgument(
       "verbose",
       help="Enable verbose output"
   )

   debug_arg = BooleanArgument(
       "debug",
       help="Enable debug mode"
   )

   no_cache_arg = BooleanArgument(
       "no-cache",
       help="Disable caching"
   )

   # Регистрация в ArgParser
   parser = ArgParser(
       processed_args=[verbose_arg, debug_arg, no_cache_arg],
       name="MyApp"
   )

**Запуск приложения:**

.. code-block:: bash

   python app.py --verbose
   python app.py --debug --no-cache
   python app.py  # без флагов

-----

.. _root_api_orchestrator_arguments_inputargument:

InputArgument
-------------

.. seealso::
   ``InputArgument`` напрямую связан с контейнером ``ArgSpace`` и является его наполнителем. Подробнее о нём см. :ref:`здесь <root_api_orchestrator_argspace>`.

Представляет собой обработанный аргумент командной строки. Этот класс используется внутри `ArgSpace` для хранения значений, полученных после парсинга.

.. py:class:: InputArgument

.. code-block:: python
   :linenos:

   __init__(self, name: str,
            value: str | Literal[True],
            founder_class: type[BaseArgument]) -> None

Создаёт экземпляр обработанного входного аргумента.

:param name: Имя аргумента
:param value: Значение аргумента. Для `BooleanArgument` — `True`, если флаг передан; для `ValueArgument` — строка со значением
:param founder_class: Класс-родитель, из которого был создан аргумент (`BooleanArgument` или `ValueArgument`)

**Атрибуты:**

.. py:attribute:: name
   :no-index:

   Имя аргумента, указанное при создании `ValueArgument` или `BooleanArgument`.

.. py:attribute:: value

   Значение аргумента. Тип зависит от исходного класса:

* Для `BooleanArgument`: `True`, если флаг был передан.
* Для `ValueArgument`: строка с переданным значением или значением по умолчанию

.. py:attribute:: founder_class

   Ссылка на класс-родитель. Используется для определения типа и фильтрации в методе `get_by_type()`.

**Методы:**

.. py:method:: __str__() -> str

   Возвращает строковое представление в формате `InputArgument(name=value)`.

   .. code-block:: python
      :linenos:

      arg = InputArgument("verbose", True, BooleanArgument)
      print(str(arg))  # InputArgument(verbose=True)

.. py:method:: __repr__() -> str

   Возвращает техническое представление объекта.