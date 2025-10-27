.. _root_api_orchestrator_arguments:

Arguments
=========

Модуль ``Arguments`` предоставляет набор классов для работы с аргументами командной строки при запуске приложения ``Argenta``. Эти аргументы позволяют настраивать поведение приложения на этапе его старта, передавая различные параметры конфигурации через интерфейс командной строки.

Аргументы регистрируются в ``ArgParser`` и парсятся при запуске приложения, становясь доступными через объект ``ArgSpace``.

-----

ValueArgument
-------------

Класс для аргументов командной строки, требующих передачи значения. Используется для параметров конфигурации, которым необходимо указать конкретное значение при запуске приложения.

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

Создает аргумент командной строки, требующий значения.

:param name: Имя аргумента
:param prefix: Префикс аргумента, по умолчанию ``--``
:param help: Сообщение справки, отображаемое при ``--help``
:param possible_values: Список допустимых значений для аргумента. Передается в параметр ``choices`` ArgumentParser
:param default: Значение по умолчанию, используемое если аргумент не передан при запуске
:param is_required: Обязатялен ли аргумент. Если ``True``, приложение не запустится без этого аргумента
:param is_deprecated: Является ли аргумент устаревшим

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

Класс для булевых аргументов командной строки, которые не требуют передачи значения. Наличие или отсутствие аргумента при запуске определяет состояние распаршенных аргументов(``True`` при наличии и ``False`` при отсутствии).

.. py:class:: BooleanArgument(BaseArgument)

.. code-block:: python
   :linenos:

   __init__(self, name: str, *,
            prefix: Literal["-", "--", "---"] = "--",
            help: str = "Help message for the boolean argument",
            is_deprecated: bool = False) -> None

Создает булевый аргумент командной строки без значения.

:param name: Имя аргумента
:param prefix: Префикс аргумента, по умолчанию ``--``
:param help: Сообщение справки, отображаемое при ``--help``
:param is_deprecated: Является ли аргумент устаревшим

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
   ``InputArgument`` непосредственно связан и является наполнителем контейнера ``ArgSpace``, подробнее про него :ref:`тут <root_api_orchestrator_argspace>`.

Представляет собой распаршенный аргумент командной строки после запуска приложения. Этот класс используется внутри объекта ``ArgSpace`` для хранения значений аргументов, полученных при парсинге.

.. py:class:: InputArgument

.. code-block:: python
   :linenos:

   __init__(self, name: str,
            value: str | Literal[True],
            founder_class: type[BaseArgument]) -> None

Создает экземпляр распарсенного входного аргумента.

:param name: Имя аргумента
:param value: Значение аргумента. Для ``BooleanArgument`` всегда ``True`` если флаг передан, для ``ValueArgument`` — строка со значением
:param founder_class: Класс-родитель, из которого был создан этот аргумент (``BooleanArgument`` или ``ValueArgument``)

**Атрибуты:**

.. py:attribute:: name

   Имя аргумента в виде строки. Соответствует имени, указанному при создании ``ValueArgument`` или ``BooleanArgument``.

.. py:attribute:: value

   Значение аргумента. Тип значения зависит от исходного класса аргумента:
   
   * Для ``BooleanArgument``: ``True`` если флаг был передан при запуске
   * Для ``ValueArgument``: строка с переданным значением или значением по умолчанию

.. py:attribute:: founder_class

   Ссылка на класс, из которого был создан этот аргумент. Используется для определения типа аргумента и фильтрации в методе ``get_by_type()``.

**Методы:**

.. py:method:: __str__() -> str

   Возвращает строковое представление аргумента в формате ``InputArgument(name=value)``.

   .. code-block:: python
      :linenos:

      arg = InputArgument("verbose", True, BooleanArgument)
      print(str(arg))  # InputArgument(verbose=True)

.. py:method:: __repr__() -> str

   Возвращает техническое представление объекта в виде строки.