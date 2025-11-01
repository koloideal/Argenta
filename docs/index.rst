.. Argenta documentation master file, created by
   sphinx-quickstart on Sat Oct 11 19:54:43 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Argenta
=======

**Библиотека для построения модульных CLI-приложений с простым и приятным API.**

Если у вас есть функциональность, которую вы хотите предоставить в виде CLI-приложения, Argenta поможет вам в этом.
Основная цель библиотеки — дать разработчикам возможность сосредоточиться на реализации своих идей, предоставляя для этого удобные абстракции.

.. image:: https://github.com/koloideal/Argenta/blob/main/imgs/mock_app_preview4.png?raw=True
   :alt: Пример приложения

Argenta предназначена для создания приложений, работающих в собственном контексте (scope). Это означает, что при запуске пользователь входит в интерактивную сессию, где ему доступна вся реализованная вами функциональность.

Один из ключевых принципов библиотеки — цикличность. После выполнения команды пользователь остаётся в интерактивной сессии, в отличие от таких библиотек, как ``argparse``, ``click`` и ``typer``. Выход из сессии контролируется самим пользователем.

**Ключевые особенности:**

* **Обработчики (Handlers)**. Компоненты, отвечающие за исполнение введённых команд. Их создание максимально декларативно.
* **Маршрутизаторы (Routers)**. Регистрируют обработчики, позволяя группировать их и задавать общие настройки.
* **Приложение (App)**. Управляет жизненным циклом приложения, подключает маршрутизаторы и настраивает утилиты, такие как автодополнение и логирование.
* **Оркестратор (Orchestrator)**. Конфигурирует, запускает и управляет всеми компонентами приложения.
* **Внедрение зависимостей**. ``Argenta`` нативно поддерживает ``dishka``, что позволяет внедрять зависимости в обработчики по типам. `Подробнее <https://dishka.readthedocs.io/en/stable/di_intro.html>`_.
* **Флаги и аргументы**. Библиотека автоматически парсит и валидирует флаги и аргументы, переданные вместе с командой.

.. toctree::
    :hidden:
    :caption: Контент:

    root/quickstart
    root/error_handling
    root/flags
    root/dependency_injection
    root/overriding_formatting
    root/redirect_stdout
    root/api/index

.. toctree::
    :hidden:
    :caption: Для разработчиков:

    root/contributing
    root/code_of_conduct

.. toctree::
    :hidden:
    :caption: Ссылки проекта:

    GitHub <https://github.com/koloideal/argenta>
    PyPI <https://pypi.org/project/argenta>
