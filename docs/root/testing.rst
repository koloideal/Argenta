Testing
=======

This section describes testing practices for applications based on ``Argenta``. Examples are based on the actual public API.

Unit Testing Handlers
---------------------

Handlers in ``Argenta`` are regular functions. They are convenient to test as pure functions without starting the entire application cycle. ``unittest`` or ``pytest`` are recommended.

**Usage example:**

.. literalinclude:: ../code_snippets/testing/simple_handler_unittest.py
   :language: python
   :linenos:
   
-----

Testing with Dependency Injection (DI)
--------------------------------------

If a handler needs dependencies, use ``dishka`` and ``Argenta`` integration:

**Usage example:**

.. literalinclude:: ../code_snippets/testing/di_handler_unittest.py
   :language: python
   :linenos:
   
-----

Integration Testing of the Application
--------------------------------------

For higher-level tests, assemble ``App`` and ``Router`` and call handlers through command parsing, bypassing the infinite input loop. This provides behavior close to reality without the need to simulate ``stdin``.

**Usage example:**

.. literalinclude:: ../code_snippets/testing/app_integration_unittest.py
   :language: python
   :linenos:
   
-----

E2E Testing of the Loop
-----------------------

Full execution of the ``start_polling`` loop can be covered through a subprocess with passing strings to ``stdin``. This is heavier and usually not required. If still necessary, an example is below.

.. danger::
    **Important:** Always pass the exit command string trigger as the last element in the ``side_effects`` list when patching ``input``.
    
    Otherwise, the application under test will wait for the next command input and will not be able to terminate correctly.

**Usage example:**

.. literalinclude:: ../code_snippets/testing/app_e2e_test.py
   :language: python
   :linenos:
   
-----

Testing Tips
------------

1. **Isolate tests**: Each test should be independent of others.
2. **Mocks for external integrations**: Replace databases, HTTP clients, etc. with stubs and ``dishka`` providers.
3. **Cover error scenarios**: Incorrect flags, unknown commands, empty input.
4. **Minimize formatting dependency**: Compare key output fragments, not the entire block.
5. **Measure coverage**: Use ``pytest-cov``.
