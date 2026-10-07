.. _root_dependency_injection:

Dependency Injection
====================

Dependency Injection (DI) is a design pattern that helps write loosely coupled, easily testable, and extensible code. Instead of handlers creating the objects (dependencies) they need themselves, they receive them from outside.

``Argenta`` uses the ``dishka`` library to implement DI, which allows you to declaratively declare dependencies directly in your handler signatures. You can read more about DI, IoC, and the API for creating providers in the `official dishka documentation <https://dishka.readthedocs.io/en/stable/di_intro.html>`_.

-----

Main Idea
---------

Imagine your handler needs access to a database to work. Instead of importing and initializing the connection inside the function, you simply declare it as an argument with a type annotation:

.. note::
   ``argenta.di.FromDishka`` is an alias for ``dishka.FromDishka``, and they are fully interchangeable.

**Usage example:**

.. literalinclude:: ../code_snippets/dependency_injection/snippet.py
   :language: python
   :linenos:

``Argenta`` with ``dishka`` will resolve the dependency by type ``Connection`` and inject it. But before using the dependency, it must be declared in a provider:

**Usage example:**

.. literalinclude:: ../code_snippets/dependency_injection/snippet2.py
   :language: python
   :linenos:
   
After creating the provider, it must be registered in the orchestrator.

.. note::
   Providers are registered in ``Orchestrator``, not in ``App``, because the orchestrator is responsible for configuring the DI container at the application level. You can pass a list of multiple providers through the ``custom_providers`` parameter.

**Usage example:**

.. literalinclude:: ../code_snippets/dependency_injection/snippet3.py
   :language: python
   :linenos:

-----

How Does It Work?
-----------------

At the implementations of DI in Argenta are **providers** and a **container**.

*   **Provider (Provider)** is a "recipe" that explains how to create and configure a particular dependency (for example, a database connection, API client, or any other service).
*   **Container (IoC Container)** is a "factory" that stores all recipes (providers) and creates and provides ready dependencies on request.

-----

Built-in Providers
------------------

``Argenta`` comes with a built-in provider that gives access to important system dependencies without additional configuration. For example, you can get the :ref:`ArgSpace <root_api_orchestrator_argspace>` object, which contains the command-line arguments passed when the application was launched.

**Usage example:**

.. literalinclude:: ../code_snippets/dependency_injection/snippet4.py
   :language: python
   :linenos:
   
-----

Data Exchange Between Handlers
------------------------------

In addition to DI, handlers can exchange data within a session through a **context object**. In ``Argenta``, this role is performed by the ``DataBridge`` object.

Each handler can write data to it, as well as read, update, and delete data.

.. seealso::
   You can read more about this in the :ref:`root_api_bridge` section.
