.. _root_api_orchestrator_arguments:

Arguments
=========

The ``Arguments`` module provides classes for working with command-line arguments. They allow configuring application behavior at startup by passing various configuration parameters.

Arguments are registered in ``ArgParser`` and after processing become available in the ``ArgSpace`` object.

-----

ValueArgument
-------------

Class for arguments that require passing a value.

.. py:class:: ValueArgument(BaseArgument)
    :no-index:

.. code-block:: python
   :linenos:

   __init__(self, name: str, *,
            prefix: Literal["-", "--", "---"] = "--",
            help: str = "Help message for the value argument",
            possible_values: list[str] | None = None,
            default: str | None = None,
            is_required: bool = False,
            is_deprecated: bool = False) -> None

Creates a command-line argument that requires a value.

:param name: Argument name
:param prefix: Prefix (defaults to ``--``)
:param help: Help message (``--help``)
:param possible_values: List of allowed values 
:param default: Default value if the argument is not passed
:param is_required: If ``True``, the argument becomes required. If not passed at startup, the application will not start
:param is_deprecated: If ``True``, marks the argument as deprecated. If passed at startup, a warning will be displayed in the console

**Usage example:**

.. literalinclude:: ../../../code_snippets/arguments/snippet.py
   :language: python
   :linenos:

**Running the application:**

.. code-block:: bash

   python app.py --host 127.0.0.1
   python app.py --host 127.0.0.1 --config custom.yaml --log-level DEBUG

-----

BooleanArgument
---------------

Class for boolean arguments that do not require a value. Their presence at startup sets the value to **True**, absence to **False**.

.. py:class:: BooleanArgument(BaseArgument)
    :no-index:

.. code-block:: python
   :linenos:

   __init__(self, name: str, *,
            prefix: Literal["-", "--", "---"] = "--",
            help: str = "Help message for the boolean argument",
            is_deprecated: bool = False) -> None

Creates a boolean command-line argument without a value.

:param name: Argument name
:param prefix: Prefix (defaults to ``--``)
:param help: Help message (``--help``)
:param is_deprecated: If ``True``, marks the argument as deprecated

**Usage example:**

.. literalinclude:: ../../../code_snippets/arguments/snippet2.py
   :language: python
   :linenos:

**Running the application:**

.. code-block:: bash

   python app.py --verbose
   python app.py --debug --no-cache
   python app.py  # without arguments

-----

.. _root_api_orchestrator_arguments_inputargument:

InputArgument
-------------

.. seealso::
   ``InputArgument`` is directly related to the ``ArgSpace`` container and serves as its filler. For more details, see :ref:`here <root_api_orchestrator_argspace>`.

Represents a processed command-line argument. This class is used inside ``ArgSpace`` to store values obtained after parsing.

.. py:class:: InputArgument
    :no-index:

.. code-block:: python
   :linenos:

   __init__(self, name: str,
            value: str | Literal[True],
            founder_class: type[BaseArgument]) -> None

Creates an instance of a processed input argument.

:param name: Argument name
:param value: Argument value. For ``BooleanArgument`` — **True** if the argument is passed, and **False** if not; for ``ValueArgument`` — the entered string 
:param founder_class: Parent class from which the argument was created (``BooleanArgument`` or ``ValueArgument``)

**Attributes:**

.. py:attribute:: name
   :no-index:

   Argument name specified when creating ``ValueArgument`` or ``BooleanArgument``.

.. py:attribute:: value

   Argument value. Type depends on the source class:

   * For ``BooleanArgument``: **True** if the argument was passed
   * For ``ValueArgument``: string with the passed value or default value

.. py:attribute:: founder_class

   Reference to the parent class. Used for type determination and filtering.
