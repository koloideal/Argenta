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
