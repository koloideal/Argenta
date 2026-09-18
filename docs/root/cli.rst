.. _root_cli:

CLI
===

Помимо библиотеки, ``Argenta`` поставляется с собственным CLI-инструментом. Он берёт на себя рутину, которая сопровождает разработку CLI-приложений: создаёт каркас проекта, запускает приложение, инспектирует зарегистрированные маршруты и собирает standalone-бинарник.

CLI поставляется как опциональная зависимость — основная библиотека остаётся лёгкой, а инструмент доступен только тем, кому он нужен.

Установка
---------

CLI доступен как опциональная зависимость ``[cli]``:

.. code-block:: shell

    pip install argenta[cli]

.. code-block:: shell

    uv add argenta[cli]

После установки команда ``argenta`` доступна в терминале:

.. code-block:: shell

    argenta --help

.. image:: https://i.ibb.co/p60T7fvh/image.png
   :alt: Argenta CLI help

.. note::
   Если ``argenta`` установлена без extras, команда ``argenta`` не будет доступна. Установите с ``[cli]``, чтобы получить доступ к CLI-инструменту.

Флаг ``--version``
~~~~~~~~~~~~~~~~~~

Показать установленную версию ``Argenta``:

.. code-block:: shell

    argenta --version

Аналогично через короткий флаг:

.. code-block:: shell

    argenta -v

-----

.. _cli_entrypoint:

Формат entrypoint
-----------------

Команды ``run``, ``routes`` и ``build`` принимают **entrypoint** — указатель на объект внутри проекта, который нужно запустить, инспектировать или собрать. Единый формат описан здесь, чтобы не повторяться в каждой команде.

Формат entrypoint:

.. code-block:: text

   <path/to/file.py>:<object_name>
   <path.to.module>:<object_name>

Поддерживаются два способа адресации:

*   **Путь к файлу** — ``app/main.py:main``. Удобно при работе с конкретным файлом.
*   **Dotted-модуль** — ``my_project.application:main``. Естественно для установленных пакетов.

Если передан путь к директории с ``__main__.py``, он разрешается автоматически — указывать файл явно не нужно.

**Примеры валидных entrypoint-ов:**

.. code-block:: text

   app/main.py:main
   app/main.py:app
   app/main.py:create_app
   my_project.application:main
   my_project/application/__main__.py:main

Тип объекта зависит от команды: ``run`` и ``build`` ожидают callable, ``routes`` — инстанс ``App`` или callable, возвращающий ``App``.

-----

Создание проектов
-----------------

Команда ``new``
~~~~~~~~~~~~~~~~

Создаёт новую директорию проекта с boilerplate-кодом. Это отправная точка: вместо ручной настройки структуры — готовый каркас за одну команду.

.. code-block:: shell

    argenta new <project_name> [--arch flat|src]

*   ``project_name`` — имя директории проекта (обязательный аргумент).
*   ``--arch`` — архитектура проекта: ``flat`` (по умолчанию) или ``src``.

**Примеры:**

.. code-block:: shell

    argenta new my-app
    argenta new my-app --arch src

При архитектуре ``flat`` создаётся следующая структура:

.. literalinclude:: ../code_snippets/cli/flat_structure.txt
   :language: text

При архитектуре ``src``:

.. literalinclude:: ../code_snippets/cli/src_structure.txt
   :language: text

.. image:: https://i.ibb.co/gY6zTQd/image.png
   :alt: argenta new command output

Команда ``init``
~~~~~~~~~~~~~~~~~

Делает то же, что и ``new``, но в текущей директории. Удобно, когда проект уже существует и нужно добавить структуру Argenta, не создавая лишний уровень вложенности.

.. code-block:: shell

    argenta init [--arch flat|src]

*   ``--arch`` — архитектура проекта: ``flat`` (по умолчанию) или ``src``.

**Примеры:**

.. code-block:: shell

    argenta init
    argenta init --arch src

.. note::
   Команда ``init`` не перезаписывает существующие файлы — они будут пропущены.

-----

Запуск приложения
-----------------

Команда ``run``
~~~~~~~~~~~~~~~~

Запускает оркестратор ``Argenta`` из callable-entrypoint. Это альтернатива прямому вызову ``python main.py``, но с автоматической настройкой окружения.

.. code-block:: shell

    argenta run <entrypoint>

Формат entrypoint — см. :ref:`Формат entrypoint <cli_entrypoint>`.

**Примеры:**

.. code-block:: shell

    argenta run app/main.py:main
    argenta run my_project.application:main

.. image:: https://i.ibb.co/fVPzxWxp/image.png
   :alt: argenta run command output

.. note::
   Команда ``run`` устанавливает переменную окружения ``RUN_FROM_ARGENTA_RUNNER=1``. ``ArgParser`` видит этот флаг и пропускает парсинг ``sys.argv``, поэтому аргументы самого ``argenta`` (типа ``--help``, ``--version``) не конфликтуют с аргументами запускаемого приложения. REPL стартует чисто, без ошибок про неизвестные флаги.

-----

Инспекция маршрутов
-------------------

Команда ``routes``
~~~~~~~~~~~~~~~~~~~

Отображает все зарегистрированные роутеры, команды, алиасы и флаги в виде дерева. Принимает как инстанс ``App``, так и callable, возвращающий ``App``.

.. code-block:: shell

    argenta routes <entrypoint>

Формат entrypoint — см. :ref:`Формат entrypoint <cli_entrypoint>`.

**Примеры:**

.. code-block:: shell

    argenta routes app/main.py:app
    argenta routes app/main.py:create_app

Инстанс ``App`` передаётся напрямую, если роутеры подключены на уровне модуля:

.. literalinclude:: ../code_snippets/cli/app_instance.py
   :language: python
   :linenos:

Фабрика ``create_app`` передаётся, если роутеры регистрируются внутри функции — например, зависят от конфига или DI:

.. literalinclude:: ../code_snippets/cli/app_factory.py
   :language: python
   :linenos:

.. note::
   При использовании callable-entrypoint REPL не запускается — фабрика вызывается, и маршруты считываются из возвращённого ``App``.

Пример вывода:

.. code-block:: text

    ──────────────────────────────────────────
       App Stats
    ──────────────────────────────────────────
    Total Routers:  1
    Total Commands: 1
    Total Aliases:  0
    Total Flags:    0
    ──────────────────────────────────────────

    📦 App object: <App>
    └── 📁 Router: Example
        └── ⚡ hello
            📝 description: Say hello

.. image:: https://i.ibb.co/wNFvKcqM/image.png
   :alt: argenta routes command output

-----

Сборка бинарника
----------------

Команда ``build``
~~~~~~~~~~~~~~~~~~

Компилирует проект в standalone-бинарник с помощью `Nuitka <https://nuitka.net/>`_, которая входит в ``[cli]`` extra.

.. code-block:: shell

    argenta build <entrypoint> [--output <name>] [-- <nuitka-flags>...]

Формат entrypoint — см. :ref:`Формат entrypoint <cli_entrypoint>`.

*   ``--output`` / ``-o`` — имя выходного бинарника (по умолчанию — имя файла или пакета).
*   ``--`` — разделитель, после которого передаются **произвольные флаги Nuitka**. Они добавляются к вызову Nuitka после аргументов Argenta, поэтому могут переопределять дефолты и добавлять любые опции, которые Nuitka поддерживает.

**Базовые примеры:**

.. code-block:: shell

    argenta build app/main.py:main
    argenta build app/main.py:main --output myapp
    argenta build app/__main__.py:main -o myapp

**Примеры с флагами Nuitka:**

.. code-block:: shell

    argenta build app/main.py:main -- --lto=yes
    argenta build app/main.py:main -- --include-package=numpy
    argenta build app/main.py:main -o myapp -- --lto=auto --include-data-files=assets/*=assets/

Что делает Argenta по умолчанию
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Команда ``build`` формирует вызов Nuitka со следующими аргументами:

*   ``--standalone --onefile`` — собирает единый бинарник со всеми зависимостями внутри.
*   ``--output-filename=<name>`` — имя выходного файла (из ``--output`` или имени entrypoint).
*   ``--jobs=<cpu_count>`` — параллельная компиляция на всех ядрах.
*   ``--lto=no`` — LTO отключён по умолчанию (быстрее сборка, медленнее запуск).
*   ``--include-windows-runtime-dlls=no`` — на Windows не включает runtime DLL в бинарник.
*   ``--python-flag=-m`` — добавляется автоматически, если entrypoint указывает на ``__main__.py``.

Все эти дефолты можно переопределить, передав соответствующий флаг после ``--``. Например, ``-- --lto=yes`` включит LTO, а ``-- --jobs=1`` отключит параллельную сборку.

Основные флаги Nuitka и их нюансы
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Полный список флагов — в `документации Nuitka <https://nuitka.net/user-documentation/user-manual.html>`_. Ниже — те, с которыми чаще всего сталкиваются при сборке CLI-приложений.

``--lto={yes,no,auto}``
    Link-Time Optimization. ``yes`` — бинарник меньше и быстрее запускается, но сборка длится заметно дольше. ``no`` (дефолт Argenta) — сборка быстрее, бинарник больше. ``auto`` — Nuitka выбирает сам. Для production-сборки имеет смысл ``yes``, для итеративной разработки — ``no``.

``--include-package=<package>``
    Явно включает пакет в бинарник. Nuitka отслеживает импорты статически, поэтому пакеты, которые импортируются динамически (через ``importlib``, плагины, ``__import__``), в бинарник не попадают — их нужно добавлять вручную. Типичные кандидаты: ``numpy``, ``pandas``, ``rich``, ``prompt_toolkit``.

``--include-data-files=<source>=<dest>``
    Включает файлы данных (шаблоны, конфиги, ассеты) в бинарник. Формат: ``--include-data-files=assets/logo.png=assets/logo.png``. Для директорий целиком — ``--include-data-dir=assets=assets``. Без этого файлы, которые приложение читает во время выполнения, не будут найдены в собранном бинарнике.

``--enable-plugin=<plugin>``
    Включает `плагин Nuitka <https://nuitka.net/user-documentation/user-manual.html#plugins>`_ для поддержки фреймворков, требующих специальной обработки. Распространённые: ``anti-bloat`` (вырезает ненужные части тяжёлых пакетов), ``numpy`` (корректная сборка с numpy), ``tk-inter`` (Tkinter GUI), ``triton`` (PyTorch triton kernels).

``--onefile`` / ``--standalone``
    ``--onefile`` (дефолт Argenta) — единый бинарник, удобный для дистрибуции. При запуске распаковывается во временную директорию, поэтому стартует медленнее. ``--standalone`` — папка с бинарником и зависимостями, стартует быстрее, но дистрибуция — это вся папка целиком. Чтобы переключиться: ``-- --standalone`` (переопределит дефолтный ``--onefile``).

``--jobs=<n>``
    Количество параллельных процессов компиляции. Дефолт Argenta — все ядра (``os.cpu_count()``). На машинах с малым объёмом памяти имеет смысл ограничить: ``-- --jobs=2``.

.. image:: https://i.ibb.co/VsVXxf7/image.png
   :alt: argenta build command output

-----

Информация об окружении
-----------------------

Команда ``info``
~~~~~~~~~~~~~~~~~

Отображает версию ``Argenta``, версию Python, платформу и ссылку на документацию.

.. code-block:: shell

    argenta info

Пример вывода:

.. code-block:: text

    Argenta 1.2.0
    Python  3.13.0
    Platform  Linux-7.1.5-zen1-2-zen-x86_64-with-glibc2.40
    Docs    https://argenta.readthedocs.io

.. image:: https://i.ibb.co/B5k8Ftyg/image.png
   :alt: argenta info command output
