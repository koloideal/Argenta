.. _root_api_orchestrator_argspace:

ArgSpace
==========

Объект ``ArgSpace`` является контейнером для хранения и управления распаршенными аргументами командной строки в приложении ``Argenta``. Его основная задача — предоставить удобный интерфейс для доступа к значениям аргументов, переданных при запуске приложения.

``ArgSpace`` автоматически создается после парсинга аргументов через ``ArgParser`` и содержит коллекцию объектов ``InputArgument``, представляющих собой финальные значения всех переданных параметров командной строки.

-----

Инициализация
-------------

.. code-block:: python
   :linenos:

   __init__(self, all_arguments: list[InputArgument]) -> None

Создает новое пространство аргументов.

* ``all_arguments`` : Список распаршенных аргументов в виде объектов ``InputArgument``. Каждый элемент содержит имя, значение и тип исходного аргумента.

**Атрибуты:**

.. py:attribute:: all_arguments

   Список всех распаршенных аргументов типа ``InputArgument``. Содержит все аргументы, переданные при запуске приложения, включая значения по умолчанию для не указанных параметров.

-----

Методы
------  

get_by_name
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_by_name(self, name: str) -> InputArgument | None

Возвращает аргумент по его имени.

:param name: Имя искомого аргумента
:return: Объект ``InputArgument`` с указанным именем или ``None``, если аргумент не найден

Метод выполняет линейный поиск по списку ``all_arguments`` и возвращает аргумент с соответствующим именем. Если аргумент не найден, возвращается ``None``.

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

Получает все аргументы определенного типа.

:param arg_type: Тип аргумента (``BooleanArgument`` или ``ValueArgument``)
:return: Список аргументов указанного типа или пустой список, если аргументы не найдены

Метод фильтрует ``all_arguments`` по атрибуту ``founder_class`` каждого ``InputArgument`` и возвращает только те аргументы, которые были созданы из указанного типа.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/argspace_snippet3.py
   :linenos:

-----

InputArgument
-------------

.. seealso ::
   Документация по ``InputArgument`` находится :ref:`тут <root_api_orchestrator_arguments_inputargument>`

-----

Примеры испольования
--------------------

``ArgSpace`` используется для доступа к значениям аргументов после запуска приложения. Типичный сценарий работы включает парсинг аргументов через ``ArgParser`` и последующее извлечение значений из ``ArgSpace``.

**Полный пример:**

.. literalinclude:: ../../../code_snippets/argspace_snippet.py
   :linenos:
   
Доступ к аргументам из хэндлеров осуществляется с помощью ``di``, подробнее :ref:`тут <root_dependency_injection>`.

.. literalinclude:: ../../../code_snippets/argspace_snippet2.py
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
