.. _root_api_orchestrator_argparser:

ArgParser
==========

``ArgParser`` предназначен для обработки **аргументов командной строки**, передаваемых приложению при запуске. Важно не путать их с флагами, которые пользователь вводит в интерактивном режиме. ``ArgParser`` позволяет получать внешнюю конфигурацию в момент старта (например, путь к файлу настроек, флаги отладки или режим запуска).

-----

Инициализация
-------------

.. code-block:: python
      :linenos:
   
      def __init__(self, processed_args: list[ValueArgument | BooleanArgument], *,
	           name: str = "Argenta",
	           description: str = "Argenta available arguments",
	           epilog: str = "github.com/koloideal/Argenta | made by kolo")

Создаёт экземпляр парсера аргументов командной строки.

* ``processed_args``: Список аргументов для обработки при запуске приложения. Подробнее см. :ref:`здесь <root_api_orchestrator_arguments>`.
* ``name``: Имя приложения для отображения в справке.
* ``description``: Описание приложения для отображения в справке.
* ``epilog``: Дополнительная информация для отображения в конце справки.

Основные методы и атрибуты
---------------------------

.. py:attribute:: parsed_argspace: ArgSpace

   Экземпляр ``ArgSpace``, содержащий все обработанные аргументы командной строки. Подробнее см. :ref:`здесь <root_api_orchestrator_argspace>`.

.. caution::
   До инициализации ``Orchestrator``, в конструктор которого был передан экземпляр ``ArgParser``, атрибут ``parsed_argspace`` будет содержать пустой ``ArgSpace``.
   
   Парсинг и валидация аргументов происходят при инициализации ``Orchestrator``, поэтому использовать ``parsed_argspace`` **целесообразно только после** этого.

-----
   
Лучшие практики
------------------------

Использовать атрибут ``parsed_argspace`` рекомендуется только на этапе настройки приложения. В обработчиках лучшей практикой является получение ``ArgSpace`` через DI. Подробнее см. :ref:`здесь <root_dependency_injection>`.

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
