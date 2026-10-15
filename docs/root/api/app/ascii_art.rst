.. _root_api_ascii_art:

Banner Fonts
============

Banner messages — ``initial_message`` at startup and ``farewell_message`` on exit — are rendered as multi-line ASCII art using `FIGlet <https://www.figlet.org/>`_ fonts (``.flf`` files). Argenta ships two bundled fonts (``tarty1`` for the welcome banner and ``chunky`` for the farewell one) and can load any ``.flf`` font from the filesystem.

.. seealso::

   :ref:`Output Formatting <root_overriding_formatting>` — the full guide: the ``.flf`` format, where to find fonts, and error handling.

-----

FigletFontLoader
----------------

.. autoclass:: argenta.app.presentation.ascii_art.FigletFontLoader
   :members:

Loads and parses ``.flf`` font files. The same loader serves both bundled and user-supplied fonts — parsing is identical, only the source differs.

**Methods:**

.. automethod:: argenta.app.presentation.ascii_art.FigletFontLoader.load

   Reads an ``.flf`` file from the filesystem and parses it into a :ref:`FigletFont <root_api_ascii_art>`. Validation happens immediately — a broken font raises before the ``App`` is created.

   :param path: Path to the ``.flf`` file (``pathlib.Path`` or ``str``).
   :raises UnreachableFigletFontException: the path does not exist or cannot be read.
   :raises InvalidFigletFontException: the file is not a well-formed ``.flf``.
   :return: Parsed ``FigletFont`` ready to be passed to ``App``.

.. automethod:: argenta.app.presentation.ascii_art.FigletFontLoader.load_bundled

   Loads one of the fonts shipped with Argenta. Used internally for the default banners; useful if you want to reuse a bundled font for custom rendering.

   :param font: A member of the ``BundledFont`` enumeration (``TARTY1`` or ``CHUNKY``).
   :return: Parsed ``FigletFont``.

-----

FigletFont
----------

.. autoclass:: argenta.app.presentation.ascii_art.FigletFont

An immutable parsed font: the glyph height and the glyph table for printable ASCII. Pass instances to ``App`` via ``initial_message_font`` / ``farewell_message_font``.

.. warning::
   ``FigletFont`` is not intended for manual construction — always obtain it through ``FigletFontLoader``, which performs validation.

-----

Error Handling
--------------

All font errors derive from a common base class, so a single ``except`` covers the whole family:

.. autoexception:: argenta.app.presentation.ascii_art.FigletFontException

.. autoexception:: argenta.app.presentation.ascii_art.UnreachableFigletFontException
   :show-inheritance:

   Raised by ``FigletFontLoader.load`` when the path does not exist or cannot be read (missing file, directory instead of a file, permission denied). Exposes the offending path via the ``path`` attribute.

.. autoexception:: argenta.app.presentation.ascii_art.InvalidFigletFontException
   :show-inheritance:

   Raised when the file parses as text but is not a well-formed ``.flf``: missing ``flf2a`` signature, malformed header, truncated glyph table, or glyph rows without endmarks. The ``reason`` attribute carries details.

.. autoexception:: argenta.app.presentation.ascii_art.MissingGlyphsException
   :show-inheritance:

   Raised at ``App`` construction when the message text contains characters the font has no glyphs for (for example, Cyrillic in an ASCII-only font). The ``missing_chars`` attribute holds the offending characters.

-----

Usage Example
-------------

.. literalinclude:: ../../../code_snippets/ascii_art/snippet.py
   :language: python
   :linenos:
