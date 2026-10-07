.. _root_api_app_autocompleter:

AutoCompleter
=============

``AutoCompleter`` is a component responsible for interactive command autocompletion. It improves user experience by offering suggestions and completing input based on command history, which speeds up work and reduces the likelihood of typos.

-----

Initialization
--------------

.. code-block:: python

  __init__(self,
           history_filename: str | None = None,
           autocomplete_button: str = "tab",
           command_highlighting: bool = True,
           auto_suggestions: bool = True) -> None:

Creates and configures an ``AutoCompleter`` instance.

* ``history_filename``: Filename for saving command history. If specified, history will be saved between sessions. When set to ``None``, history is stored only within the session context.
* ``autocomplete_button``: Key that activates autocompletion. Defaults to **Tab**.
* ``command_highlighting``: If True, then in real time, when entering a  command, it will be highlighted: green if such a trigger exists and red if not.
* ``auto_suggestions``: If True, the addition to the previously entered  command will immediately be displayed in light gray in the input line.

-----

Purpose and Features
--------------------

Main features of ``AutoCompleter``:

*   **History-based autocompletion**: When the autocompletion key is pressed (by default **Tab**), the system searches history for commands starting with the already entered text.

*   **Common prefix**: If multiple commands with a common prefix are found, only the common part will be inserted. For example, for commands ``show_users`` and ``show_profile``, when entering ``sho`` and pressing **Tab**, the input will be completed to ``show_``.

*   **Persistent history**: If ``history_filename`` is specified, command history is saved to a file on exit and loaded on the next startup. This makes autocompletion "smarter" over time.

*   **Key customization**: The autocompletion key can be changed using the ``autocomplete_button`` parameter.
 
-----

Usage Example
-------------

``AutoCompleter`` is passed as an argument when initializing `App`.

.. literalinclude:: ../../../code_snippets/autocompleter/snippet.py
    :language: python
    :linenos:
