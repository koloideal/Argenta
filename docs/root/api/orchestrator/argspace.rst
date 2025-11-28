.. _root_api_orchestrator_argspace:

ArgSpace
==========

``ArgSpace`` — это контейнер для хранения и управления обработанными аргументами командной строки. Его основная задача — предоставить удобный интерфейс для доступа к значениям, переданным при запуске приложения.

``ArgSpace`` создаётся автоматически после обработки аргументов с помощью ``ArgParser`` и содержит коллекцию объектов ``InputArgument``.

-----

Инициализация
-------------

Создание экземпляров класса ``ArgSpace`` происходит под `капотом`, вам не нужно создавать их вручную.

**Атрибуты:**

.. py:attribute:: all_arguments

   Список всех обработанных аргументов типа ``InputArgument``.

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
:return: Объект ``InputArgument`` или ``None``, если аргумент не найден.

**Пример использования:**

.. literalinclude:: ../../../code_snippets/argspace/snippet4.py
   :linenos:

-----

get_by_type
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_by_type(self, arg_type: type[BaseArgument]) -> list[InputArgument] | list[Never]

Возвращает все аргументы определённого типа.

:param arg_type: Тип аргумента (``BooleanArgument`` или ``ValueArgument``).
:return: Список аргументов указанного типа или пустой список.

Метод фильтрует ``all_arguments`` по атрибуту ``founder_class`` и возвращает аргументы, созданные из указанного типа.

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

``ArgSpace`` используется для доступа к значениям аргументов после запуска приложения. Типичный сценарий включает обработку аргументов через ``ArgParser`` и последующее извлечение значений из ``ArgSpace``.

**Полный пример:**

.. literalinclude:: ../../../code_snippets/argspace/snippet.py
   :linenos:
   
Доступ к аргументам из обработчиков осуществляется с помощью ``di``. Подробнее см. :ref:`здесь <root_dependency_injection>`.

.. literalinclude:: ../../../code_snippets/argspace/snippet2.py
   :linenos:

**Запуск приложения:**

.. code-block:: bash

   python server.py --host 0.0.0.0 --port 9000
   # Output:
   # Server configuration:
   #   Host: 0.0.0.0
   #   Port: 9000
