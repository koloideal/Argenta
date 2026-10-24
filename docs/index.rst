.. Argenta documentation master file, created by
   sphinx-quickstart on Sat Oct 11 19:54:43 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Argenta
=======

What is it and why?
-------------------

**The command-driven framework for Python: build your commands once, run them in any runtime.**

If you have functionality that you want to provide as a command-driven application, Argenta will help you with that. The main goal of the framework is to enable developers to focus on implementing their ideas by providing convenient abstractions.

.. image:: /_static/app-screenshot.png
   :alt: App example

Argenta separates the **command layer** from the way it is consumed. Routers, commands and flags are declared once; a **runtime** then decides how people or programs interact with them. Two runtimes ship out of the box, and the same ``main()`` serves both — the choice is made at launch, commands never depend on the runtime:

*   **REPL runtime** — a cyclic interactive session in the terminal, similar to a Python REPL or a MySQL console: the application starts once and the user executes commands one after another, unlike ``argparse``, ``click`` or ``typer``, where the process terminates after each command. Exiting the session is controlled by the user.
*   **A2UI runtime** — exposes the same commands as a generated `A2UI <https://a2ui.org/>`_ surface (one card per command, one input per flag) streamed to renderers over SSE, WebSocket, gRPC and other transports. See :ref:`A2UI Runtime <root_a2ui>`.

**Key features:**

*   **Pluggable runtimes**: The application emits semantic output blocks (banner, command output, errors) and a runtime decides how to present them — so the interface (terminal, web UI, your own runtime) stays decoupled from the logic. See :ref:`Runtimes <root_runtimes>`.
*   **Interactive sessions**: The REPL runtime keeps the session alive between commands — users execute commands sequentially without restarting the application.
*   **Declarative syntax**: Commands and their handlers are declared using simple decorators, making the code intuitive and allowing you to focus on "what" you want to do, not "how".
*   **Native DI**: Thanks to integration with `dishka <https://dishka.readthedocs.io/en/stable/>`_, you can easily inject dependencies directly into command handlers, simplifying their testing, avoiding mutable globals, and much more.
*   **Automatic validation and parsing**: The library handles command-line flags and arguments, including their parsing, validation, and type conversion.
*   **Flexible configuration**: You can easily customize system messages, output formatting, create custom handlers for non-standard behavior, and more.

-----

Architecture and lifecycle
--------------------------

The following diagram illustrates how Argenta components interact with each other while processing user input.

.. image:: /_static/architecture.png
   :alt: Request Lifecycle Diagram
   :align: center

.. toctree::
    :hidden:
    :caption: Content:

    root/quickstart
    root/runtimes
    root/error_handling
    root/flags
    root/api/index

.. toctree::
    :hidden:
    :caption: Advanced usage:

    root/repl/index
    root/a2ui/index
    root/dependency_injection
    root/cli
    root/testing

.. toctree::
    :hidden:
    :caption: For developers:

    root/contributing
    root/code_of_conduct
    root/metrics

.. toctree::
    :hidden:
    :caption: Project links:

    GitHub <https://github.com/koloideal/argenta>
    PyPI <https://pypi.org/project/argenta>
