.. _root_api_orchestrator_argspace:

ArgSpace
==========

``ArgSpace`` — это контейнер для хранения и управления обработанными аргументами командной строки. Его основная задача — предоставить удобный интерфейс для доступа к значениям, переданным при запуске приложения.

``ArgSpace`` создаётся автоматически после обработки аргументов с помощью `ArgParser` и содержит коллекцию объектов `InputArgument`.

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

   __init__(self, all_arguments: list[InputArgument]) -> None

Создаёт новое пространство аргументов.

* ``all_arguments``: Список обработанных аргументов в виде объектов `InputArgument`. Каждый элемент содержит имя, значение и тип исходного аргумента.

**Атрибуты:**

.. py:attribute:: all_arguments

   Список всех обработанных аргументов типа `InputArgument`, включая значения по умолчанию для не указанных параметров.

-----

Методы
------  

get_by_name
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_by_name(self, name: str) -> InputArgument | None

Возвращает аргумент по имени.

:param name: Имя искомого аргумента.
:return: Объект `InputArgument` или `None`, если аргумент не найден.

Метод выполняет линейный поиск по списку `all_arguments`. Если аргумент не найден, возвращается `None`.

**Пример использования:**

.. code-block:: python
   :linenos:

   # Получение значения конкретного аргумента
   config_arg = argspace.get_by_name("config")
   if config_arg:
       print(f"Config path: {config_arg.value}")
   
   verbose_arg = argspace.get_by_name("verbose")
   if verbose_arg and verbose_arg.value:
       print("Verbose mode enabled")
   
   # Обработка отсутствующего аргумента
   unknown_arg = argspace.get_by_name("nonexistent")
   if unknown_arg is None:
       print("Argument not found")

-----

get_by_type
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_by_type(self, arg_type: type[BaseArgument]) -> list[InputArgument] | list[Never]

Возвращает все аргументы определённого типа.

:param arg_type: Тип аргумента (`BooleanArgument` или `ValueArgument`).
:return: Список аргументов указанного типа или пустой список.

Метод фильтрует `all_arguments` по атрибуту `founder_class` и возвращает аргументы, созданные из указанного типа.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/argspace/snippet3.py
   :linenos:

-----

InputArgument
-------------

.. seealso ::
   Документация по ``InputArgument`` находится :ref:`здесь <root_api_orchestrator_arguments_inputargument>`.

-----

Примеры испольования
--------------------

`ArgSpace` используется для доступа к значениям аргументов после запуска приложения. Типичный сценарий включает обработку аргументов через `ArgParser` и последующее извлечение значений из `ArgSpace`.

**Полный пример:**

.. literalinclude:: ../../../code_snippets/argspace/snippet.py
   :linenos:
   
Доступ к аргументам из обработчиков осуществляется с помощью DI. Подробнее см. :ref:`здесь <root_dependency_injection>`.

.. literalinclude:: ../../../code_snippets/argspace/snippet2.py
   :linenos:

**Запуск приложения:**

.. code-block:: bash

   # С параметрами по умолчанию
   python server.py
   # Output:
   # Server configuration:
   #   Host: localhost
   #   Port: 8080

   # С кастомными параметрами
   python server.py --host 0.0.0.0 --port 9000
   # Output:
   # Server configuration:
   #   Host: 0.0.0.0
   #   Port: 9000
