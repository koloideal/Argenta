.. _root_api_orchestrator_argparser:

ArgParser
==========

Объект ``ArgParser`` в ``Argenta`` предназначен для разбора и обработки **аргументов командной строки**, которые передаются вашему приложению при его запуске. Важно не путать их с флагами команд, которые пользователь вводит в интерактивном режиме работы приложения. ``ArgParser`` позволяет вашему приложению получать внешнюю конфигурацию в момент старта, например, путь к файлу настроек, флаги для отладки или режим запуска.

-----

Инициализация
-------------

.. code-block:: python
      :linenos:
   
      def __init__(self, processed_args: list[ValueArgument | BooleanArgument], *,
	           name: str = "Argenta",
	           description: str = "Argenta available arguments",
	           epilog: str = "github.com/koloideal/Argenta | made by kolo")

Создает экземпляр парсера аргументов командной строки.

* ``processed_args``: Список аргументов, которые будут обрабатываться и парситься при запуске приложения, подробнее :ref:`тут <root_api_orchestrator_arguments>`.
* ``name``: Имя приложения, которое будет отображаться в справке.
* ``description``: Описание приложения, которое будет отображаться в справке.
* ``epilog``: Дополнительная информация, которая будет отображаться в конце справки.

Основные методы и атрибуты
---------------------------

.. py:attribute:: parsed_argspace: ArgSpace

   Экземпляр класса ``ArgSpace``, который содержит все обработанные аргументы командной строки, подробнее :ref:`тут <root_api_orchestrator_argspace>`.

.. caution::
   До инициализации инстанса ``Orchestrator``, которому в конструктор был передан соответствующий экземпляр ``ArgParser``, атрибут ``parsed_argspace`` будет равен пустому ``ArgSpace``.
   
   Парсинг и валидация аргументов командной строки происходит при инициализации ``Orchestrator``, соответственно использование атрибута ``parsed_argspace`` **целесообразно только после инициализации** ``Orchestrator``.

-----
   
Лучшие практики
------------------------

Использование атрибута ``parsed_argspace`` рекомендуется только на этапе настройки приложения, в хэндлерах лучшей практикой является получение ``ArgSpace`` через ``di``,  подробнее :ref:`тут <root_dependency_injection>`.

Пример использования
--------------------

.. literalinclude:: ../../../code_snippets/argparser/snippet.py
   :language: python
   :linenos:
   
Обработка ошибок
----------------

.. seealso:: 
   Про типы аргументов подробнее в :ref:`Arguments <root_api_orchestrator_arguments>`

При работе с аргументами командной строки стандартный ``ArgumentParser`` автоматически обрабатывает следующие ситуации:

**Отсутствие обязательного аргумента:**

.. code-block:: bash

    $ python app.py
    usage: MyApp [-h] --config CONFIG
    MyApp: error: the following arguments are required: --config

**Недопустимое значение из списка choices:**

.. code-block:: bash

    $ python app.py --config app.yaml --log-level TRACE
    usage: MyApp [-h] --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
    MyApp: error: argument --log-level: invalid choice: 'TRACE'

**Использование устаревшего аргумента:**

При использовании аргумента с ``is_deprecated=True`` выводится предупреждение, но выполнение продолжается:

.. code-block:: bash

    $ python app.py --old-param value
    Warning: argument --old-param is deprecated
