.. _root_api_orchestrator_argparser:

ArgParser
=========

``ArgParser`` is designed for processing **command-line arguments** passed to the application at startup. It's important not to confuse them with flags that the user enters in interactive mode. ``ArgParser`` allows receiving external configuration at startup (e.g., path to settings file, debug flags, or launch mode).

-----

Initialization
--------------

.. code-block:: python
      :linenos:
   
      def __init__(self, processed_args: list[ValueArgument | BooleanArgument], *,
	           name: str = "Argenta",
	           description: str = "Argenta available arguments",
	           epilog: str = "github.com/koloideal/Argenta | made by kolo")

Creates an instance of the command-line argument parser.

* ``processed_args``: List of arguments to process at application startup. For more details, see :ref:`here <root_api_orchestrator_arguments>`.
* ``name``: Application name for display in help.
* ``description``: Application description for display in help.
* ``epilog``: Additional information for display at the end of help.

-----

Attributes
----------

.. py:attribute:: parsed_argspace: ArgSpace

   ``ArgSpace`` instance containing all processed command-line arguments. For more details, see :ref:`here <root_api_orchestrator_argspace>`.

.. caution::
   Before initializing ``Orchestrator``, to whose constructor an ``ArgParser`` instance was passed, the ``parsed_argspace`` attribute will contain an empty ``ArgSpace``.
   
   Parsing and validation of arguments occur during ``Orchestrator`` initialization, so using ``parsed_argspace`` is **advisable only after** that.
   
-----

Best Practices
--------------

Using the ``parsed_argspace`` attribute is recommended only during the application setup phase. In handlers, the best practice is to obtain ``ArgSpace`` through DI. For more details, see :ref:`here <root_dependency_injection>`.

**Usage example:**

.. literalinclude:: ../../../code_snippets/argparser/snippet.py
   :language: python
   :linenos:
   
Error Handling
--------------

.. seealso:: 
   For more details on argument types, see :ref:`Arguments <root_api_orchestrator_arguments>`

When working with command-line arguments, the standard ``ArgumentParser`` automatically handles the following situations:

**Missing required argument:**

.. code-block:: bash

    $ python app.py
    usage: Argenta [-h] --config CONFIG
    Argenta: error: the following arguments are required: --config

**Invalid value from possible_values list:**

.. code-block:: bash

    $ python app.py --config app.yaml --log-level TRACE
    usage: Argenta [-h] --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
    Argenta: error: argument --log-level: invalid choice: 'TRACE'

**Using a deprecated argument:**

When using an argument with ``is_deprecated=True``, a warning is displayed, but execution continues:

.. code-block:: bash

    $ python app.py --old-param value
    Warning: argument --old-param is deprecated

.. warning::

    The parameter is supported since CPython 3.13; on earlier versions it is ignored.

