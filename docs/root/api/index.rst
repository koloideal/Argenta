.. _root_api_index:


Public API
==========

Section Description
-------------------

This section describes the library's public API. It includes:

- Classes and functions for integration into your applications.
- Usage recommendations and supported scenarios.
- Code examples, detailed signatures, and descriptions of return values.
- Stability and backward compatibility guarantees.

Interfaces not described in this section are considered internal. Using them may lead to errors when updating the library. When developing your own solutions, use only the components described here. This will ensure the stability and compatibility of your products with future versions of ``Argenta``.

-----

Public Imports
--------------

All main library components are available for direct import from the root package ``argenta`` or its submodules.

.. rubric:: Main Components

.. code-block:: python

   from argenta import App, Orchestrator, Router, Command, Response

* :ref:`App <root_api_app_index>` — Application object responsible for routing logic, settings, validation, etc.
* :ref:`Orchestrator <root_api_orchestrator_index>` — Class for configuring and launching the entire application.
* :ref:`Router <root_api_router>` — Class for grouping and registering commands.
* :ref:`Command <root_api_command_index>` — Class for creating commands when initializing handlers.
* :ref:`Response <root_api_response>` — Response object passed to handlers.

.. rubric:: Commands and Flags

.. code-block:: python

   from argenta.command import (
       Flag, 
       Flags, 
       InputFlag,
       InputFlags, 
       PossibleValues,
       ValidationStatus,
       PredefinedFlags
   )

* :ref:`Flag <root_api_command_flag>` — Class for describing a flag.
* :ref:`Flags <root_api_command_flags>` — Collection for registering flags.
* :ref:`InputFlag <root_api_command_input_flag>` — Class for a user-entered flag.
* :ref:`InputFlags <root_api_command_input_flags>` — Collection of entered flags.
* :ref:`PossibleValues <root_api_command_possible_values>` — Validation rules for flag values.
* :ref:`ValidationStatus <root_api_command_validation_status>` — Flag validation statuses.
* :ref:`PredefinedFlags <root_api_command_flag_predefined_flags>` — Collection of predefined flags.

.. rubric:: Application Configuration

.. code-block:: python

   from argenta.app import (
       AutoCompleter, 
       StaticDividingLine, 
       DynamicDividingLine,
       PredefinedMessages
   )

* :ref:`AutoCompleter <root_api_app_autocompleter>` - Class for configuring autocompletion.
* :ref:`StaticDividingLine <root_api_app_dividing_lines>` — Static dividing line for output formatting.
* :ref:`DynamicDividingLine <root_api_app_dividing_lines>` — Dynamic dividing line for output formatting.
* :ref:`PredefinedMessages <root_api_predefined_messages>` — Ready-made messages for output at application startup.

.. rubric:: Dependency Injection

.. code-block:: python

   from argenta.di import (
       FromDishka,
       inject
   )

* :ref:`FromDishka <root_dependency_injection>` — Marker for a function argument as a dependency that should be injected.
* :ref:`inject <root_dependency_injection>` — Decorator for injecting dependencies specified in the signature.


.. toctree::
    :hidden:
    
    app/index
    router
    orchestrator/index
    command/index
    response
    bridge