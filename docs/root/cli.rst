.. _root_cli:

Командная строка
==================

Помимо библиотеки, ``Argenta`` поставляется с собственным CLI-инструментом, который помогает создавать проекты, запускать приложения, инспектировать маршруты и собирать бинарники.

Установка
---------

CLI доступен как опциональная зависимость:

.. code-block:: shell

    pip install argenta[cli]

После установки команда ``argenta`` доступна в терминале:

.. code-block:: shell

    argenta --help

.. image:: _static/cli/help.png
   :alt: Argenta CLI help

.. note::
   Если вы устанавливали ``argenta`` без extras, CLI-инструмент не будет доступен. Установите с ``[cli]`` для доступа к команде ``argenta``.

Флаг ``--version``
~~~~~~~~~~~~~~~~~~~

Показать установленную версию ``Argenta``:

.. code-block:: shell

    argenta --version

.. code-block:: shell

    argenta -v

-----

Создание проектов
-----------------

Команда ``new``
~~~~~~~~~~~~~~~~

Создаёт новую директорию проекта с boilerplate-кодом.

.. code-block:: shell

    argenta new <project_name> [--with-arch flat|src]

*   ``project_name`` — имя директории проекта (обязательный аргумент).
*   ``--with-arch`` — архитектура проекта: ``flat`` (по умолчанию) или ``src``.

**Примеры:**

.. code-block:: shell

    argenta new my-app
    argenta new my-app --with-arch src

При архитектуре ``flat`` создаётся следующая структура:

.. literalinclude:: ../code_snippets/cli/flat_structure.txt
   :language: text

При архитектуре ``src``:

.. literalinclude:: ../code_snippets/cli/src_structure.txt
   :language: text

.. image:: _static/cli/new_command.png
   :alt: argenta new command output

Команда ``init``
~~~~~~~~~~~~~~~~~

Инициализирует boilerplate в текущей директории. Удобно, когда проект уже существует и нужно добавить структуру Argenta.

.. code-block:: shell

    argenta init [--with-arch flat|src]

*   ``--with-arch`` — архитектура проекта: ``flat`` (по умолчанию) или ``src``.

**Примеры:**

.. code-block:: shell

    argenta init
    argenta init --with-arch src

.. note::
   Команда ``init`` не перезаписывает существующие файлы — они будут пропущены.

-----

Запуск приложений
-----------------

Команда ``run``
~~~~~~~~~~~~~~~~

Запускает оркестратор ``Argenta`` из callable-ентрипойнта. Это альтернатива прямому вызову ``python main.py``, но с автоматической настройкой окружения.

.. code-block:: shell

    argenta run <entrypoint>

*   ``entrypoint`` — путь к callable в формате ``<path/to/file.py>:<callable>`` или ``<path.to.module>:<callable>``.

**Примеры:**

.. code-block:: shell

    argenta run app/main.py:main
    argenta run my_project.application:main

.. image:: _static/cli/run_command.png
   :alt: argenta run command output

.. note::
   Команда ``run`` устанавливает переменную окружения ``RUN_FROM_ARGENTA_RUNNER=1``, что отключает парсинг аргументов командной строки в ``ArgParser``. Это позволяет запустить REPL без конфликтов с CLI-аргументами ``argenta``.

-----

Инспекция маршрутов
-------------------

Команда ``routes``
~~~~~~~~~~~~~~~~~~~

Отображает все зарегистрированные роутеры, команды, алиасы и флаги в виде дерева. Принимает как инстанс ``App``, так и callable, возвращающий ``App``.

.. code-block:: shell

    argenta routes <entrypoint>

*   ``entrypoint`` — путь к ``App`` или callable в формате ``<path/to/file.py>:<app_or_callable>``.

**Примеры:**

.. code-block:: shell

    argenta routes app/main.py:app
    argenta routes app/main.py:create_app

Если передан инстанс ``App``:

.. literalinclude:: ../code_snippets/cli/app_instance.py
   :language: python
   :linenos:

Если передан callable (фабрика), он будет вызван, и результат будет использован для отображения маршрутов:

.. literalinclude:: ../code_snippets/cli/app_factory.py
   :language: python
   :linenos:

.. image:: _static/cli/routes_command.png
   :alt: argenta routes command output

.. note::
   При использовании callable-ентрипойнта (например, ``create_app``) REPL не запускается — фабрика вызывается, и маршруты считываются из возвращённого ``App``. Это полезно, когда роутеры подключаются внутри функции, а не на уровне модуля.

-----

Сборка бинарников
-----------------

Команда ``build``
~~~~~~~~~~~~~~~~~~

Компилирует проект в standalone-бинарник с помощью `Nuitka <https://nuitka.net/>`_.

.. code-block:: shell

    argenta build <entrypoint> [--output <name>]

*   ``entrypoint`` — путь к callable в формате ``<path/to/file.py>:<callable>``.
*   ``--output`` / ``-o`` — имя выходного бинарника (по умолчанию — имя файла или пакета).

**Примеры:**

.. code-block:: shell

    argenta build app/main.py:main
    argenta build app/main.py:main --output myapp
    argenta build app/__main__.py:main -o myapp

.. warning::
   Для использования команды ``build`` необходимо установить ``Nuitka``:

   .. code-block:: shell

       pip install nuitka

.. image:: _static/cli/build_command.png
   :alt: argenta build command output

-----

Информация об окружении
-----------------------

Команда ``info``
~~~~~~~~~~~~~~~~~

Отображает версию ``Argenta``, версию Python, платформу и ссылку на документацию.

.. code-block:: shell

    argenta info

.. image:: _static/cli/info_command.png
   :alt: argenta info command output

-----

Формат ентрипойнтов
-------------------

Все команды, принимающие ентрипойнт (``run``, ``routes``, ``build``), используют единый формат:

.. code-block:: text

   <path/to/file.py>:<object_name>
   <path.to.module>:<object_name>

Поддерживаются как пути к файлам, так и dotted-модули. Если передан путь к директории с ``__main__.py``, он будет разрешён автоматически.

**Примеры валидных ентрипойнтов:**

.. code-block:: text

   app/main.py:main
   app/main.py:app
   app/main.py:create_app
   my_project.application:main
   my_project/application/__main__.py:main
