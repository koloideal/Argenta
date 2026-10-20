.. _root_api_orchestrator_index:

Orchestrator
============

``Orchestrator`` is a high-level component that configures and orchestrates the application, command-line parser, DI, and other components at the same hierarchical level as ``App``.

While ``App`` is responsible for interactive session logic (command input, routing), ``Orchestrator`` prepares the environment for its operation and serves as the entry point to the application.

-----

Initialization
--------------

.. autoclass:: argenta.Orchestrator

Creates and configures an ``Orchestrator`` instance.

* ``arg_parser``: ``ArgParser`` instance responsible for parsing command-line arguments at script startup (not to be confused with commands in interactive mode).
* ``custom_providers``: List of custom ``dishka.Provider`` providers for adding your services (e.g., database connections or API clients) to the DI container.
* ``auto_inject_handlers``: If **True** (default), ``dishka`` will automatically inject dependencies into command handlers by inspecting their signatures.

-----

Main Methods
------------

.. automethod:: argenta.Orchestrator.run_repl

   This is the main method that starts the application. It launches an infinite input -> output loop.

   :param app: ``App`` instance to be launched.
   :param config: optional :ref:`REPLConfig <root_api_repl>` — terminal layout of the REPL (dividing line, gaps). Ignored when the app runs as an A2UI agent.

   .. note::
      When the process is started via ``argenta a2ui`` (``ARGENTA_RUN_MODE=a2ui``), ``run_repl`` delegates to ``run_agent`` over the transport selected by the CLI flags — the same ``main()`` serves both runtimes. See :ref:`A2UI Runtime <root_a2ui>`.

-----

.. automethod:: argenta.Orchestrator.run_agent

   Runs the application as an `A2UI <https://a2ui.org/>`_ agent: the registered commands are emitted as a declarative surface and incoming ``action`` messages are dispatched through the regular command-handling path.

   :param app: ``App`` instance to be launched.
   :param transport: a :ref:`Transport <root_api_a2ui>` implementation carrying the JSON messages.
   :param config: optional :ref:`A2UIConfig <root_api_a2ui>` — surface and envelope configuration.
   :param verbose: log the agent lifecycle to stderr.

-----

.. autoclass:: argenta.orchestrator.config.RunnerConfig

Frozen dataclass describing the **environment bridge** between the ``argenta`` CLI commands and the orchestrator: the CLI sets these variables, the orchestrator reads them. Override the field values to rename the variables or change the defaults (host ``127.0.0.1``, port ``8765``, the ``a2ui`` mode marker). For the semantics of each variable see :ref:`the environment bridge <root_a2ui>`.

-----
   
Purpose and Usage
-----------------

``Orchestrator`` abstracts the complexity associated with setting up DI and parsing startup arguments.

This approach separates responsibilities: ``App`` is responsible for interactive session logic, while ``Orchestrator`` handles environment preparation and application launch.

**Usage example:**

.. literalinclude:: ../../../code_snippets/orchestrator/snippet.py
   :language: python

.. toctree::
    :hidden:

    argparser
    arguments
    argspace
