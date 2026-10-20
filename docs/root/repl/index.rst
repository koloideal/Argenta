.. _root_repl:

REPL Runtime
============

The **REPL runtime** is the default way an ``Argenta`` app is consumed: a cyclic interactive session in the terminal. The application starts once and the user executes commands one after another — like a Python REPL or a MySQL console — without restarting the process for every command. Exiting is controlled by the user, not by the framework.

How the session works
---------------------

``REPLRuntime`` drives a read-eval-print loop:

1.  Startup — the app registers its system router, shows the banner and startup messages, then prints the command groups (repeated before every input if ``repeat_command_groups_printing`` is on).
2.  The autocompleter is initialized with the registered triggers.
3.  The loop — render the prompt, read a line, parse and dispatch it through the same path every runtime uses.
4.  The loop ends when the exit command is dispatched (``q`` by default).

Terminal presentation — dividing lines around command and system output, gaps between blocks — is configured through :ref:`REPLConfig <root_api_repl>`.

-----

Running
-------

From ``main()``
~~~~~~~~~~~~~~~

``Orchestrator.run_repl(app, config=None)`` starts the session:

.. code-block:: python

   from argenta import App, Orchestrator
   from argenta.repl import REPLConfig, DynamicDividingLine

   app = App()
   # ... include routers ...

   if __name__ == "__main__":
       Orchestrator().run_repl(app, REPLConfig(dividing_line=DynamicDividingLine("~")))

The ``config`` argument is the :ref:`REPLConfig <root_api_repl>` — the terminal layout: dividing line, prompt gap, output frame padding, gaps around startup messages and command groups. All fields have defaults; omitting it gives the standard look.

.. note::
   When the process is launched via ``argenta a2ui``, ``run_repl`` delegates to the A2UI runtime and the REPL config is ignored — the same ``main()`` serves both runtimes. See :ref:`the environment bridge <root_a2ui>`.

With the CLI
~~~~~~~~~~~~

The ``argenta repl`` command (``[cli]`` extra) runs an entrypoint without touching ``python main.py``, with optional hot reload:

.. code-block:: shell

    argenta repl app/main.py:main           # start the session
    argenta repl app/main.py:main --reload  # restart on .py changes

It sets ``RUN_FROM_ARGENTA_RUNNER=1`` so ``ArgParser`` skips ``sys.argv`` — the CLI's own flags never leak into the app. Entrypoint format and options: :ref:`the CLI section <root_cli>`.

-----

Terminal interaction
--------------------

*   **Prompt** — ``App.prompt`` rendered through the app renderer and read via ``prompt_toolkit``, with autocompletion of command triggers.
*   **Ctrl+C** — discards the current input and re-prompts; it does not crash the session.
*   **Ctrl+D / EOF** — routes through the exit-command handler (same as typing ``q``), including the end of a piped stdin.
*   ``input()`` inside handlers — needs ``Router(disable_redirect_stdout=True)`` so the prompt is not buffered; see :ref:`root_redirect_stdout`.

-----

Layout and formatting
---------------------

Terminal presentation details live in the pages below — they are all REPL-runtime specifics and irrelevant to other runtimes:

.. toctree::
   :maxdepth: 1

   redirect_stdout
   overriding_formatting

*   :ref:`Overriding standard output <root_redirect_stdout>` — how ``stdout`` capture enables dynamic dividing lines, and when to disable it.
*   :ref:`Output formatting <root_overriding_formatting>` — rich vs plain system messages, FIGlet banner fonts, custom printers.

API reference: :ref:`REPLConfig, REPLRuntime, TerminalLayout, dividing lines <root_api_repl>`.
