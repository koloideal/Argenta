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

*   **Интерактивные сессии**. В отличие от традиционных CLI-инструментов, Argenta создаёт циклические сессии, позволяя пользователю выполнять команды последовательно, не перезапуская приложение.
*   **Декларативный синтаксис**. Команды и их обработчики объявляются с помощью простых декораторов, что делает код чистым и интуитивно понятным.
*   **Встроенное внедрение зависимостей (DI)**. Благодаря интеграции с `dishka <https://dishka.readthedocs.io/en/stable/>`_, вы можете легко внедрять сервисы (например, подключения к БД) прямо в обработчики команд, что упрощает их тестирование и переиспользование.
*   **Автоматическая валидация и парсинг**. Библиотека берёт на себя обработку флагов и аргументов командной строки, включая их парсинг, валидацию и преобразование типов.
*   **Гибкая настройка**. Вы можете легко кастомизировать системные сообщения, форматирование вывода и даже перенаправлять стандартный вывод (stdout) в свои обработчики.

Архитектура и жизненный цикл
-----------------------------

Следующая диаграмма иллюстрирует, как компоненты Argenta взаимодействуют друг с другом, обрабатывая ввод пользователя.

.. graphviz::

   digraph "Request Lifecycle" {
      rankdir=LR;
      node [shape=box, style=rounded, fontname="sans-serif"];
      edge [fontname="sans-serif"];

      subgraph cluster_input {
          label = "Пользовательский ввод";
          style=filled;
          color=lightgrey;
          node [style=filled,color=white];
          "User Input" [label="Ввод команды"];
      }

      subgraph cluster_core {
          label = "Ядро Argenta";
          style=filled;
          color=lightblue;
          node [style=filled,color=white];
          "Orchestrator";
          "App";
          "Router";
          "Command Handler" [label="Обработчик команды"];
      }

      subgraph cluster_di {
          label = "Внедрение зависимостей";
          style=filled;
          color=lightgreen;
          node [style=filled,color=white];
          "DI Container (dishka)" [label="DI-контейнер (dishka)"];
          "Dependencies" [label="Зависимости (напр., Repository)"];
      }

      subgraph cluster_output {
          label = "Вывод";
          style=filled;
          color=lightgrey;
          node [style=filled,color=white];
          "User Output" [label="Вывод результата"];
      }

      "User Input" -> "Orchestrator" [label="1. Запуск и парсинг"];
      "Orchestrator" -> "App" [label="2. Передача управления"];
      "App" -> "Router" [label="3. Поиск нужного роутера"];
      "Router" -> "Command Handler" [label="4. Вызов обработчика"];
      "Command Handler" -> "DI Container (dishka)" [label="5. Запрос зависимостей"];
      "DI Container (dishka)" -> "Dependencies" [label="6. Создание и предоставление"];
      "Dependencies" -> "Command Handler" [label="7. Внедрение"];
      "Command Handler" -> "App" [label="8. Формирование ответа"];
      "App" -> "User Output" [label="9. Отображение результата"];
   }


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
