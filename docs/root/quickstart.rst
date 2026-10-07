.. _root_quickstart:

Quick Start
===========

In this guide, we will look at two examples of creating a CLI application with Argenta:

*   **Simple example**: a minimal application for quick introduction to the main components.
*   **Medium-complexity example**: the Calculator app using and setting flags.
*   **More complex example**: a full-featured "Task Manager" application with dependency injection and business logic.

Simple Example
--------------

**Installation**

.. code-block:: shell

    pip install argenta

This example demonstrates the absolute minimum required to create and run an application. You can copy this code, run it, and immediately see the result.

.. literalinclude:: ../code_snippets/quickstart/simple_app.py
   :language: python
   :linenos:

**Running**

Save the code to a file (for example, ``main.py``) and run:

.. code-block:: shell

    python main.py

**Result**

.. image:: https://i.ibb.co/35q24Bh8/image.png
   :alt: Simple App Example
   
-----

Intermediate Example: Calculator with Flags
-------------------------------------------

Before moving to a complex example with DI, let's consider an intermediate option — a calculator that uses flags to control behavior.

.. literalinclude:: ../code_snippets/quickstart/calculator_app.py
   :language: python
   :linenos:

**Running:**

Save the code to a file ``calculator.py`` and run:

.. code-block:: shell

    python calculator.py

**Usage:**

.. code-block:: shell

   calc --a 10 --b 5 --operation add
   calc --a 10 --b 5 --operation mul

This example shows how to work with flags without using DI. Now let's move on to a more complex example.

-----

Complex Example: Task Manager with DI
-------------------------------------

In this guide, we will create a full-featured CLI application "Task Manager" that will demonstrate working with dependency injection.

1. **Installation**

.. code-block:: shell

    pip install argenta

2. **Defining Data Models and Repository**

First, let's define data models for tasks and a repository to store them.

.. literalinclude:: ../code_snippets/quickstart/task_manager/repository.py
   :language: python
   :linenos:

3. **Creating a Provider for DI**

To allow Argenta to inject ``TaskRepository`` into our handlers, we will create a provider for ``dishka``.

.. literalinclude:: ../code_snippets/quickstart/task_manager/provider.py
   :language: python
   :linenos:

4. **Creating Command Handlers**

Now let's create handlers for the ``add-task`` and ``list-tasks`` commands. Notice how we use flags and inject ``TaskRepository``.

.. literalinclude:: ../code_snippets/quickstart/task_manager/handlers.py
   :language: python
   :linenos:

5. **Building and Running the Application**

Finally, let's put it all together: create an ``App`` instance, connect the router and provider, and then run the application.

.. literalinclude:: ../code_snippets/quickstart/task_manager/main.py
   :language: python
   :linenos:

6. **Result**

Now you can run ``main.py`` and interact with your new CLI application.

.. image:: https://i.ibb.co/bgsCLZhP/image.png
   :alt: Task Manager Example
