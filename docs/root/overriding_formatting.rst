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

Welcome (``initial_message``) and farewell (``farewell_message``) messages are displayed as ASCII art by default, rendered with `FIGlet <https://www.figlet.org/>`_ fonts.

.. warning::
   The bundled fonts cover printable ASCII only and **do not support Cyrillic**. If a message contains characters missing from the font, ``MissingGlyphsException`` is raised when the ``App`` is created. For Cyrillic messages, provide a font with the needed glyphs (see below) or disable formatting using ``override_system_messages=True``.

Custom Fonts
------------

What is an .flf font
~~~~~~~~~~~~~~~~~~~~

``Argenta`` renders banners in the `FIGlet <https://www.figlet.org/>`_ font format — the same one used by the classic ``figlet`` CLI and thousands of community fonts. An ``.flf`` file is a plain text file with a strict structure:

*   **Header line** — starts with ``flf2a`` followed by a *hardblank* character, then space-separated fields: glyph height, baseline, max line length, layout mode and comment count.
*   **Comment lines** — free-form metadata (author, license, description).
*   **Glyph table** — a fixed-height block of rows per printable ASCII character (codes 32–126), in order. Every row ends with an *endmark* character (conventionally ``@``, doubled on the last row of a glyph); the hardblank marks a space that must survive rendering.

A small fragment of a glyph table (font height 4, endmark ``@``):

.. code-block:: text

       $@
      $ $@
      $$  @@
    __ __ $@
   / / / /|@
  | | | | @@

Because the format is decades old and fully textual, font files are easy to inspect, version-control and diff — and there is a huge existing collection to pick from.

Where to get fonts
~~~~~~~~~~~~~~~~~~

*   The official `FIGlet font database <https://www.figlet.org/fontdb.cgi>`_ — hundreds of fonts, previewed online.
*   The `pyfiglet fonts collection <https://github.com/pwaller/pyfiglet/tree/master/pyfiglet/fonts>`_ on GitHub.
*   Any ``figlet`` package installed on your system (``/usr/share/figlet/`` on most Linux distros).

The CLI can browse community collections and download fonts directly:

.. code-block:: bash

   argenta fonts list                          # list fonts available for download
   argenta fonts fetch slant                   # downloads slant.flf (+ compiled .flfd)
   argenta fonts fetch slant -o fonts/         # save into a specific directory
   argenta fonts fetch https://example.com/doom.flf   # direct URL also works

Argenta bundles two fonts: ``tarty1`` for ``initial_message`` and ``chunky`` for ``farewell_message``.

The typical workflow end to end: find a font (``argenta fonts list`` or the sources above), download it (``argenta fonts fetch``), load it into your ``App`` — and, when you are ready to ship a standalone binary, compile it into ``.flfd`` so the banner costs nothing at startup.

Loading a custom font
~~~~~~~~~~~~~~~~~~~~~

Load an ``.flf`` file with ``FigletFontLoader`` and pass the result to ``App``:

.. code-block:: python
   :linenos:

   from pathlib import Path

   from argenta import App
   from argenta.app.presentation.ascii_art import FigletFontLoader

   font_loader = FigletFontLoader()
   app = App(
       initial_message="Argenta",
       initial_message_font=font_loader.load(Path("fonts/slant.flf")),
       farewell_message_font=font_loader.load(Path("fonts/mini.flf")),
   )

Fonts are loaded eagerly at ``App`` creation, so a broken font fails immediately, not mid-session.

Compiled fonts (.flfd)
~~~~~~~~~~~~~~~~~~~~~~

Fonts are loaded eagerly when the ``App`` is created — font loading sits directly on the startup path of your CLI, and parsing an ``.flf`` file takes a noticeable fraction of a millisecond per font. To make font loading nearly free, ``FigletFontLoader`` maintains a compiled dump next to the source file:

*   ``load("fonts/slant.flf")`` looks for ``fonts/slant.flfd`` first. If the dump is present, has a valid header and matches the source file's modification time, it is deserialized directly — no parsing.
*   If the dump is missing, corrupted or stale, the ``.flf`` is parsed and the dump is (re)written automatically, so the next load is fast.
*   ``load("fonts/slant.flfd")`` loads a dump directly. A standalone ``.flfd`` with no ``.flf`` beside it works too — this is the recommended way to ship fonts when packaging your app into a binary.

To compile a font ahead of time (for example before building a standalone binary), use the CLI:

.. code-block:: bash

   argenta fonts compile fonts/slant.flf                 # writes fonts/slant.flfd
   argenta fonts compile fonts/slant.flf -o dist/slant.flfd

The equivalent is available in Python as ``FigletFontLoader.compile(source, target)``.

.. warning::
   ``.flfd`` files contain serialized data intended only for fonts you compiled yourself or received bundled with Argenta. Never pass a ``.flfd`` obtained from an untrusted source to ``load`` — stick to plain ``.flf`` for third-party fonts, which is validated field by field.

Error handling
~~~~~~~~~~~~~~

All font errors derive from ``FigletFontException``:

*   ``UnreachableFigletFontException`` — the path does not exist or cannot be read.
*   ``InvalidFigletFontException`` — the file is not a well-formed ``.flf`` (bad signature, malformed header, truncated glyph table, rows without endmarks).
*   ``MissingGlyphsException`` — the font lacks glyphs for characters in the message (raised at ``App`` construction).

See the :ref:`API reference <root_api_ascii_art>` for details.

Limitations
~~~~~~~~~~~

*   Smushing rules from the font header are ignored — glyphs are laid out at full width, matching the classic ``banner``-style output.
*   Only the printable-ASCII glyph table is required to be present; characters outside it are reported via ``MissingGlyphsException``.

-----

Output Customization
--------------------

For complete replacement of text output logic, the ``App`` constructor provides the ``printer`` parameter.

*   **printer**: ``Callable[[str], None]`` This parameter allows passing any callable entity (for example, a function) that will be used to output all system messages. By default, this is ``rich.console.Console().print``. You can pass your own function here to, for example, log output to a file or send it over the network.

.. important::
   When overriding the output function, you should ensure it supports ``rich`` markup, otherwise system messages will be output in raw form. In this case, it is recommended to override standard formatting using ``override_system_messages=True``.
