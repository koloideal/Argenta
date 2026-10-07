.. _root_cli:

CLI
===

In addition to the library, ``Argenta`` ships with its own CLI tool. It takes over the routine that surrounds CLI app development: scaffolds a project, runs the application, inspects registered routes, and builds a standalone binary.

The CLI is shipped as an optional dependency — the core library stays light, and the tool is available only to those who need it.

Installation
------------

The CLI is available as the optional ``[cli]`` dependency:

.. code-block:: shell

    pip install argenta[cli]

.. code-block:: shell

    uv add argenta[cli]

After installation, the ``argenta`` command is available in the terminal:

.. code-block:: shell

    argenta --help

.. image:: https://i.ibb.co/p60T7fvh/image.png
   :alt: Argenta CLI help

.. note::
   If ``argenta`` is installed without extras, the ``argenta`` command will not be available. Install with ``[cli]`` to get access to the CLI tool.

The ``--version`` flag
~~~~~~~~~~~~~~~~~~~~~~

Show the installed ``Argenta`` version:

.. code-block:: shell

    argenta --version

Equivalently, via the short flag:

.. code-block:: shell

    argenta -v

-----

.. _cli_entrypoint:

Entrypoint format
-----------------

The ``run``, ``routes`` and ``build`` commands accept an **entrypoint** — a pointer to an object inside the project to run, inspect, or build. The shared format is documented here once instead of repeating it in each command.

Entrypoint format:

.. code-block:: text

   <path/to/file.py>:<object_name>
   <path.to.module>:<object_name>

Two addressing styles are supported:

*   **File path** — ``app/main.py:main``. Convenient when working with a specific file.
*   **Dotted module** — ``my_project.application:main``. Natural for installed packages.

If a directory path containing ``__main__.py`` is passed, it is resolved automatically — no need to name the file explicitly.

**Examples of valid entrypoints:**

.. code-block:: text

   app/main.py:main
   app/main.py:app
   app/main.py:create_app
   my_project.application:main
   my_project/application/__main__.py:main

The expected object type depends on the command: ``run`` and ``build`` expect a callable, ``routes`` expects an ``App`` instance or a callable returning ``App``.

-----

Scaffolding projects
--------------------

The ``new`` command
~~~~~~~~~~~~~~~~~~~

Creates a new project directory with boilerplate code. It is the starting point: instead of setting up the structure by hand, a ready-made skeleton in a single command.

.. code-block:: shell

    argenta new <project_name> [--arch flat|src]

*   ``project_name`` — project directory name (required argument).
*   ``--arch`` — project architecture: ``flat`` (default) or ``src``.

**Examples:**

.. code-block:: shell

    argenta new my-app
    argenta new my-app --arch src

With the ``flat`` architecture, the following structure is created:

.. literalinclude:: ../code_snippets/cli/flat_structure.txt
   :language: text

With the ``src`` architecture:

.. literalinclude:: ../code_snippets/cli/src_structure.txt
   :language: text

.. image:: https://i.ibb.co/gY6zTQd/image.png
   :alt: argenta new command output

The ``init`` command
~~~~~~~~~~~~~~~~~~~~

Does the same as ``new``, but in the current directory. Convenient when the project already exists and the Argenta structure needs to be added without introducing an extra level of nesting.

.. code-block:: shell

    argenta init [--arch flat|src]

*   ``--arch`` — project architecture: ``flat`` (default) or ``src``.

**Examples:**

.. code-block:: shell

    argenta init
    argenta init --arch src

.. note::
   The ``init`` command does not overwrite existing files — they are skipped.

-----

Running an application
----------------------

The ``run`` command
~~~~~~~~~~~~~~~~~~~

Starts the ``Argenta`` orchestrator from a callable entrypoint. It is an alternative to calling ``python main.py`` directly, but with automatic environment setup.

.. code-block:: shell

    argenta run <entrypoint>

Entrypoint format — see :ref:`Entrypoint format <cli_entrypoint>`.

**Examples:**

.. code-block:: shell

    argenta run app/main.py:main
    argenta run my_project.application:main

.. image:: https://i.ibb.co/fVPzxWxp/image.png
   :alt: argenta run command output

.. note::
   The ``run`` command sets the ``RUN_FROM_ARGENTA_RUNNER=1`` environment variable. ``ArgParser`` sees this flag and skips parsing ``sys.argv``, so the ``argenta`` arguments themselves (such as ``--help``, ``--version``) do not conflict with the arguments of the application being launched. The REPL starts cleanly, with no errors about unknown flags.

-----

Inspecting routes
-----------------

The ``routes`` command
~~~~~~~~~~~~~~~~~~~~~~

Displays all registered routers, commands, aliases, and flags as a tree. Accepts either an ``App`` instance or a callable returning ``App``.

.. code-block:: shell

    argenta routes <entrypoint>

Entrypoint format — see :ref:`Entrypoint format <cli_entrypoint>`.

**Examples:**

.. code-block:: shell

    argenta routes app/main.py:app
    argenta routes app/main.py:create_app

An ``App`` instance is passed directly when routers are registered at the module level:

.. literalinclude:: ../code_snippets/cli/app_instance.py
   :language: python
   :linenos:

A ``create_app`` factory is passed when routers are registered inside a function — for example, when they depend on config or DI:

.. literalinclude:: ../code_snippets/cli/app_factory.py
   :language: python
   :linenos:

.. note::
   When a callable entrypoint is used, the REPL is not started — the factory is called, and routes are read from the returned ``App``.

Example output:

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

Building a binary
-----------------

The ``build`` command
~~~~~~~~~~~~~~~~~~~~~

Compiles a project into a standalone binary using `Nuitka <https://nuitka.net/>`_, which is included in the ``[cli]`` extra.

.. code-block:: shell

    argenta build <entrypoint> [--output <name>] [-- <nuitka-flags>...]

Entrypoint format — see :ref:`Entrypoint format <cli_entrypoint>`.

*   ``--output`` / ``-o`` — output binary name (defaults to the file or package name).
*   ``--`` — a separator after which **arbitrary Nuitka flags** are passed. They are appended to the Nuitka invocation after Argenta's arguments, so they can override defaults and add any options Nuitka supports.

**Basic examples:**

.. code-block:: shell

    argenta build app/main.py:main
    argenta build app/main.py:main --output myapp
    argenta build app/__main__.py:main -o myapp

**Examples with Nuitka flags:**

.. code-block:: shell

    argenta build app/main.py:main -- --lto=yes
    argenta build app/main.py:main -- --include-package=numpy
    argenta build app/main.py:main -o myapp -- --lto=auto --include-data-files=assets/*=assets/

What Argenta does by default
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``build`` command assembles a Nuitka invocation with the following arguments:

*   ``--standalone --onefile`` — builds a single binary with all dependencies bundled inside.
*   ``--output-filename=<name>`` — output file name (from ``--output`` or the entrypoint name).
*   ``--jobs=<cpu_count>`` — parallel compilation across all cores.
*   ``--lto=no`` — LTO is disabled by default (faster build, slower startup).
*   ``--include-windows-runtime-dlls=no`` — on Windows, runtime DLLs are not bundled into the binary.
*   ``--python-flag=-m`` — added automatically when the entrypoint points at a ``__main__.py``.

Any of these defaults can be overridden by passing the corresponding flag after ``--``. For example, ``-- --lto=yes`` enables LTO, and ``-- --jobs=1`` disables parallel compilation.

Key Nuitka flags and their trade-offs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The full flag list is in the `Nuitka documentation <https://nuitka.net/user-documentation/user-manual.html>`_. Below are the ones most often encountered when building CLI applications.

``--lto={yes,no,auto}``
    Link-Time Optimization. ``yes`` — the binary is smaller and starts faster, but the build takes noticeably longer. ``no`` (Argenta's default) — faster build, larger binary. ``auto`` — Nuitka decides. For production builds ``yes`` makes sense; for iterative development, ``no``.

``--include-package=<package>``
    Explicitly includes a package in the binary. Nuitka tracks imports statically, so packages imported dynamically (via ``importlib``, plugins, ``__import__``) do not end up in the binary — they must be added by hand. Common candidates: ``numpy``, ``pandas``, ``rich``, ``prompt_toolkit``.

``--include-data-files=<source>=<dest>``
    Includes data files (templates, configs, assets) into the binary. Format: ``--include-data-files=assets/logo.png=assets/logo.png``. For whole directories — ``--include-data-dir=assets=assets``. Without this, files the application reads at runtime will not be found inside the built binary.

``--enable-plugin=<plugin>``
    Enables a `Nuitka plugin <https://nuitka.net/user-documentation/user-manual.html#plugins>`_ for frameworks that need special handling. Common ones: ``anti-bloat`` (strips unneeded parts of heavy packages), ``numpy`` (correct numpy bundling), ``tk-inter`` (Tkinter GUI), ``triton`` (PyTorch triton kernels).

``--onefile`` / ``--standalone``
    ``--onefile`` (Argenta's default) — a single binary, convenient for distribution. It unpacks into a temporary directory on startup, so it starts slower. ``--standalone`` — a folder with the binary and its dependencies; starts faster, but distribution means shipping the whole folder. To switch: ``-- --standalone`` (overrides the default ``--onefile``).

``--jobs=<n>``
    Number of parallel compilation processes. Argenta's default is all cores (``os.cpu_count()``). On memory-constrained machines it makes sense to limit it: ``-- --jobs=2``.

.. image:: https://i.ibb.co/VsVXxf7/image.png
   :alt: argenta build command output

-----

Environment information
-----------------------

The ``info`` command
~~~~~~~~~~~~~~~~~~~~

Displays the ``Argenta`` version, Python version, platform, and a link to the documentation.

.. code-block:: shell

    argenta info

Example output:

.. code-block:: text

    Argenta 1.2.0
    Python  3.13.0
    Platform  Linux-7.1.5-zen1-2-zen-x86_64-with-glibc2.40
    Docs    https://argenta.readthedocs.io

.. image:: https://i.ibb.co/B5k8Ftyg/image.png
   :alt: argenta info command output
