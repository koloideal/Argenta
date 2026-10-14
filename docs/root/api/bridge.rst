.. _root_api_bridge:

DataBridge
==========

``DataBridge`` is an entity that provides temporary data storage that exists within a single application session (from startup to exit). It is designed for data exchange between handlers.

The main way to access ``DataBridge`` is through DI.

.. code-block:: python
   :linenos:

   from argenta.di import FromDishka
   from argenta import DataBridge, Response
   
   # ... setting up router and other

   def my_handler(response: Response, data_bridge: FromDishka[DataBridge]):
       # ... your code

**Practical Example: Authentication**

Let's consider an example where the `login` command saves an authentication token, and the `get-profile` command uses it.

.. literalinclude:: ../../code_snippets/response/data_sharing.py
   :language: python
   :linenos:

**How it works:**

1.  When calling a handler, ``dishka`` automatically injects a ``DataBridge`` instance.
2.  The ``login --username <name>`` command calls ``login_handler``, which saves the token through the injected ``data_bridge``.
3.  The ``get-profile`` command calls ``get_profile_handler``, which also receives ``data_bridge`` and extracts the token from it.

-----------

.. autoclass:: argenta.DataBridge

   Initializes the storage. When used through DI, it is called automatically.

.. automethod:: argenta.DataBridge.update

   Updates the storage with data from a dictionary.

.. automethod:: argenta.DataBridge.get_all

   Returns all data from the storage.

.. automethod:: argenta.DataBridge.get_by_key

   Returns the value by key or ``None`` if the key is not found.

.. automethod:: argenta.DataBridge.delete_by_key

   Deletes the value by key. Raises ``KeyError`` if the key is not found.

.. automethod:: argenta.DataBridge.clear_all

   Completely clears the storage.
