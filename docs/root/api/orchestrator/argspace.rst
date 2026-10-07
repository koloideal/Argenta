.. _root_api_orchestrator_argspace:

ArgSpace
========

``ArgSpace`` is a container for storing and managing processed command-line arguments. Its main purpose is to provide a convenient interface for accessing values passed at application startup.

``ArgSpace`` is created automatically after processing arguments using ``ArgParser`` and contains a collection of ``InputArgument`` objects.

-----

Initialization
--------------

Creation of ``ArgSpace`` class instances happens under the hood, you don't need to create them manually.

**Attributes:**

.. py:attribute:: all_arguments

   List of all processed arguments of type ``InputArgument``.

-----

Methods
-------

get_by_name
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_by_name(self, name: str) -> InputArgument | None

Returns an argument by name.

:param name: Name of the argument to search for.
:return: ``InputArgument`` object or ``None`` if the argument is not found.

**Usage example:**

.. literalinclude:: ../../../code_snippets/argspace/snippet4.py
   :linenos:

-----

get_by_type
~~~~~~~~~~~

.. code-block:: python
   :linenos:

   get_by_type(self, arg_type: type[BaseArgument]) -> list[InputArgument] | list[Never]

Returns all arguments of a specific type.

:param arg_type: Argument type (``BooleanArgument`` or ``ValueArgument``).
:return: List of arguments of the specified type or an empty list.

The method filters ``all_arguments`` by the ``founder_class`` attribute and returns arguments created from the specified type.

**Usage example:**

.. literalinclude:: ../../../code_snippets/argspace/snippet3.py
   :linenos:

-----

InputArgument
-------------

.. seealso ::
   Documentation for ``InputArgument`` is located :ref:`here <root_api_orchestrator_arguments_inputargument>`.

-----

Usage Examples
--------------

``ArgSpace`` is used to access argument values after the application starts. A typical scenario includes processing arguments through ``ArgParser`` and subsequent extraction of values from ``ArgSpace``.

**Complete example:**

.. literalinclude:: ../../../code_snippets/argspace/snippet.py
   :linenos:
   
Access to arguments from handlers is done using DI. For more details, see :ref:`here <root_dependency_injection>`.

**Usage example:**

.. literalinclude:: ../../../code_snippets/argspace/snippet2.py
   :linenos:

**Running the application:**

.. code-block:: bash

   python server.py --host 0.0.0.0 --port 9000
   # Output:
   # Server configuration:
   #   Host: 0.0.0.0
   #   Port: 9000
