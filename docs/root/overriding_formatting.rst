.. _root_overriding_formatting:

Output Formatting
=================

By default, ``Argenta`` uses the ``rich`` library for text output with enhanced formatting. It allows applying colors and styles, creating tables, highlighting syntax, and much more, which improves the visual perception of information.

------

Managing Standard Formatting
----------------------------

When creating an ``App`` instance, you can use the ``override_system_messages: bool`` parameter (default ``False``), which allows disabling standard formatting.

If set to ``True``, text styling and ASCII graphics will be disabled, and system messages will be output in "raw" form.

-----

Welcome and Farewell Messages
-----------------------------

Welcome (``initial_message``) and farewell (``farewell_message``) messages are displayed as ASCII art by default.

.. warning::
   The ``art`` library is designed to work with ASCII characters and **does not support Cyrillic**. This leads to distortion of Russian and other Cyrillic alphabet characters. If your message contains Cyrillic, it is recommended to disable formatting using ``override_system_messages=True`` or use only Latin characters.

-----

Output Customization
--------------------

For complete replacement of text output logic, the ``App`` constructor provides the ``printer`` parameter.

*   **printer**: ``Callable[[str], None]`` This parameter allows passing any callable entity (for example, a function) that will be used to output all system messages. By default, this is ``rich.console.Console().print``. You can pass your own function here to, for example, log output to a file or send it over the network.

.. important::
   When overriding the output function, you should ensure it supports ``rich`` markup, otherwise system messages will be output in raw form. In this case, it is recommended to override standard formatting using ``override_system_messages=True``.
