.. _root_api_index:


Публичное API
=============

Описание раздела
----------------

В этом разделе описан публичный API библиотеки. Он включает:

- Классы и функции для интеграции в ваши приложения.
- Рекомендации по использованию и поддерживаемые сценарии.
- Примеры кода, подробные сигнатуры и описание возвращаемых значений.
- Гарантии стабильности и обратной совместимости.

Интерфейсы, не описанные в этом разделе, считаются внутренними. Их использование может привести к ошибкам при обновлении библиотеки. При разработке собственных решений используйте только компоненты, описанные здесь. Это обеспечит стабильность и совместимость ваших продуктов с будущими версиями ``Argenta``.

-----

Публичные импорты
-----------------

Все основные компоненты библиотеки доступны для прямого импорта из корневого пакета ``argenta`` или его подмодулей.

.. rubric:: Основные компоненты

.. code-block:: python

   from argenta import (
       App, Orchestrator, Router, Command, Response
   )

* :ref:`App <root_api_app_index>` — Основной класс приложения.
* :ref:`Orchestrator <root_api_orchestrator_index>` — Класс для управления жизненным циклом.
* :ref:`Router <root_api_router>` — Класс для группировки и регистрации команд.
* :ref:`Command <root_api_command_index>` — Класс для создания команд.
* :ref:`Response <root_api_response>` — Объект ответа, передаваемый в обработчики.

.. rubric:: Команды и флаги

.. code-block:: python

   from argenta.command import (
       Flag, 
       Flags, 
       InputFlag,
       InputFlags, 
       PossibleValues,
       ValidationStatus,
       PredefinedFlags
   )

* :ref:`Flag <root_api_command_flag>` — Класс для описания флага.
* :ref:`Flags <root_api_command_flags>` — Коллекция для регистрации флагов.
* :ref:`InputFlag <root_api_command_input_flag>` — Класс для введённого пользователем флага.
* :ref:`InputFlags <root_api_command_input_flags>` — Коллекция введённых флагов.
* :ref:`PossibleValues <root_api_command_possible_values>` — Правила валидации значений флагов.
* :ref:`ValidationStatus <root_api_command_validation_status>` — Статусы валидации флагов.
* ``PredefinedFlags`` — Готовые наборы флагов (например, ``--help``).

.. rubric:: Настройка приложения

.. code-block:: python

   from argenta.app import (
       AutoCompleter, 
       StaticDividingLine, 
       DynamicDividingLine,
       PredefinedMessages
   )

* :ref:`AutoCompleter <root_api_app_autocompleter>` — Базовый класс для автодополнения.
* :ref:`StaticDividingLine <root_api_app_dividing_lines>` — Статическая разделительная линия.
* :ref:`DynamicDividingLine <root_api_app_dividing_lines>` — Динамическая разделительная линия.
* ``PredefinedMessages`` — Готовые системные сообщения.

.. rubric:: Внедрение зависимостей

.. code-block:: python

   from argenta.di import (
       FromDishka,
       inject
   )

* :ref:`FromDishka <root_dependency_injection>` — Маркер для внедрения зависимостей.
* :ref:`inject <root_dependency_injection>` — Декоратор для асинхронного внедрения.


.. toctree::
    :hidden:
    
    app/index
    router
    orchestrator/index
    command/index
    response
    