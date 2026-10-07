.. Argenta documentation master file, created by
   sphinx-quickstart on Sat Oct 11 19:54:43 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Argenta
=======

What is it and why?
-------------------

**A library for building modular CLI applications with a simple and pleasant API.**

If you have functionality that you want to provide as a CLI application, Argenta will help you with that. The main goal of the library is to enable developers to focus on implementing their ideas by providing convenient abstractions.

.. image:: https://i.ibb.co/fzWcfgFq/2025-12-04-173045.png
   :alt: App example

Argenta is designed for creating applications that work in their own context (scope). This means that the application starts once and creates an interactive session, similar to Python REPL or MySQL console. When launched, the user enters this session where all the functionality you've implemented is available.

One of the key principles of the library is cyclicity. After executing a command, the user remains in the interactive session, unlike libraries such as ``argparse``, ``click``, and ``typer``, where the application terminates after each command. Exiting the session is controlled by the user.

**Key features:**

*   **Interactive sessions**: Unlike traditional CLI tools, ``Argenta`` creates cyclical sessions, allowing users to execute commands sequentially without restarting the application.
*   **Declarative syntax**: Commands and their handlers are declared using simple decorators, making the code intuitive and allowing you to focus on "what" you want to do, not "how".
*   **Native DI**: Thanks to integration with `dishka <https://dishka.readthedocs.io/en/stable/>`_, you can easily inject dependencies directly into command handlers, simplifying their testing, avoiding mutable globals, and much more.
*   **Automatic validation and parsing**: The library handles command-line flags and arguments, including their parsing, validation, and type conversion.
*   **Flexible configuration**: You can easily customize system messages, output formatting, create custom handlers for non-standard behavior, and more.

-----

Architecture and lifecycle
--------------------------

The following diagram illustrates how Argenta components interact with each other while processing user input.

.. image:: https://i.ibb.co/hF3FdFr1/argenta-intro-drawio-2.png
   :alt: Request Lifecycle Diagram
   :align: center

.. toctree::
    :hidden:
    :caption: Content:

    root/quickstart
    root/error_handling
    root/flags
    root/overriding_formatting
    root/api/index

.. toctree::
    :hidden:
    :caption: Advanced usage:

    root/redirect_stdout
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
