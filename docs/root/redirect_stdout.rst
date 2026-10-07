.. _root_redirect_stdout:

Overriding Standard Output
==========================

``Argenta`` provides flexible mechanisms for output formatting, including dynamic dividing lines. This is achieved by intercepting the standard output stream (``stdout``), which imposes certain specifics.

-----

When to Disable stdout Interception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Disable ``stdout`` interception (``disable_redirect_stdout=True`` in ``Router``) if your commands:

✓ Use ``input()`` for interactive user input 

✓ Use progress bars (``tqdm``, ``rich.progress``) 

✓ Output data in real-time (streaming, logs) 

✓ Use libraries that work directly with ``stdout`` 

For regular commands with ``print()``, interception can be left enabled — it does not affect their operation.

-----

``stdout`` Interception Mechanism
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, ``Argenta`` intercepts all text output to ``stdout`` inside a command handler. This is necessary to implement **dynamic dividers**: the system analyzes the output, finds the longest line, and uses it to draw the top and bottom borders. This approach creates a neat interface where the command output is "wrapped" in a frame fitted to its content.

Example of an application with a dynamic dividing line:

.. image:: https://i.ibb.co/yn9rWnNC/2025-11-07-180751.png
  :alt: Example of an application with a dynamic dividing line

As you can see, the dividing line is exactly the same length as the longest line in the output.

The same application with a static line:

.. image:: https://i.ibb.co/P8B4xyp/2025-11-07-180330.png
  :alt: Example of an application with a static dividing line

In this example, the dividing line has a fixed length (25 characters by default).

-----

Side Effects of ``stdout`` Interception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A side effect of this mechanism manifests when using functions that sequentially output text to the console and expect user input. A classic example is the standard ``input()`` function.

.. code-block:: python
    :linenos:

    user_name = input("Enter your name: ")
    print(f"Hello, {user_name}!")

.. warning::
   With ``stdout`` interception enabled, text (for example, ``"Enter your name: "``) **will not be output to the console immediately**. It will go into a buffer and appear only after the handler finishes, along with the rest of the output. This can confuse the user.

-----

Disabling ``stdout`` Interception with ``disable_redirect_stdout``
------------------------------------------------------------------

To solve this problem, the ``Router`` constructor provides a special argument:

*   **disable_redirect_stdout** (``bool``, default ``False``)

If you set ``disable_redirect_stdout=True`` when creating a router, the ``stdout`` interception mechanism will be disabled for all its handlers.

**Usage example:**

.. literalinclude:: ../code_snippets/redirect_stdout/sample.py
   :language: python
   :linenos:

In this case, ``input()`` will work as usual, and the user will immediately see the input prompt.

-----

Types of Dividing Lines
-----------------------

``Argenta`` supports two types of dividers, which are configured during ``App`` initialization:

1.  **``DynamicDividingLine()``**
	*  Default behavior. The line length dynamically adjusts to the longest text in the output.
	*  Requires enabled ``stdout`` interception (``disable_redirect_stdout=False`` in the router).

2.  **``StaticDividingLine(length: int = 25)``**
	*  The line has a fixed length (25 characters by default), which can be set via the ``length`` argument.
	*  Used forcibly for routers with ``disable_redirect_stdout=True``, as it is impossible to determine dynamic length without output interception.

-----

Configuring the Dividing Line in ``App``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can globally set the divider type for the entire application via the ``dividing_line`` argument in the ``App`` constructor.

**Usage example:**

.. literalinclude:: ../code_snippets/redirect_stdout/sample2.py
   :language: python
   :linenos:

-----

Resulting Behavior
------------------

.. list-table::
   :widths: 25 25 35 15
   :header-rows: 1

   * - ``disable_redirect_stdout`` on ``Router``
     - Line type in ``App``
     - Actual behavior
     - Does ``input()`` work correctly?
   * - ``False`` (default)
     - ``DynamicDividingLine``
     - Dynamic line, length by content
     - No
   * - ``False`` (default)
     - ``StaticDividingLine``
     - Static line of specified length
     - No
   * - ``True``
     - ``DynamicDividingLine``
     - **Forcibly static line** (default length)
     - Yes
   * - ``True``
     - ``StaticDividingLine``
     - Static line of specified length
     - Yes

Thus, for interactive commands that require user input, disable ``stdout`` interception at the router level. For all other commands, you can leave the default behavior.
