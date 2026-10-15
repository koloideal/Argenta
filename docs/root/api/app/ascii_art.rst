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

   Loads a font from the filesystem. Given an ``.flf`` path, a compiled ``.flfd`` dump sitting next to it is used when present and up to date, and (re)written otherwise — see :ref:`Output Formatting <root_overriding_formatting>` for the details. ``.flfd`` paths are also accepted directly. Validation happens immediately — a broken font raises before the ``App`` is created.

   :param path: Path to the ``.flf`` or ``.flfd`` file (``pathlib.Path`` or ``str``).
   :raises UnreachableFigletFontException: the path does not exist or cannot be read.
   :raises InvalidFigletFontException: the file is not a well-formed ``.flf`` or ``.flfd``.
   :return: Parsed ``FigletFont`` ready to be passed to ``App``.

.. automethod:: argenta.app.presentation.ascii_art.FigletFontLoader.compile

   Compiles an ``.flf`` font into an ``.flfd`` dump. Equivalent to the ``argenta fonts compile`` CLI command; useful for building compiled fonts programmatically before packaging an application.

   :param source_path: Path to the source ``.flf`` file (``pathlib.Path`` or ``str``).
   :param target_path: Optional output path; defaults to ``<source>.flfd`` next to the source.
   :raises UnreachableFigletFontException: the source cannot be read or the target cannot be written.
   :raises InvalidFigletFontException: the source is not a well-formed ``.flf``.
   :return: Path to the written ``.flfd`` file.

.. automethod:: argenta.app.presentation.ascii_art.FigletFontLoader.load_bundled

   Loads one of the fonts shipped with Argenta. Used internally for the default banners; useful if you want to reuse a bundled font for custom rendering.

   :param font: A member of the ``BundledFont`` enumeration (``TARTY1`` or ``CHUNKY``).
   :return: Parsed ``FigletFont``.

-----

FigletFontFetcher
-----------------

.. autoclass:: argenta.app.presentation.ascii_art.FigletFontFetcher

Downloads fonts from the community collections known to Argenta (the upstream ``figlet`` repository and the `figlet-fonts <https://github.com/xero/figlet-fonts>`_ collection) or from a direct URL. Powers the ``argenta fonts`` CLI commands.

**Methods:**

.. automethod:: argenta.app.presentation.ascii_art.FigletFontFetcher.fetch

   Downloads a font by name (trying the known collections, including capitalized spellings) or from a direct URL. The downloaded file is validated and a compiled ``.flfd`` dump is written next to it automatically. Invalid content is rejected and the file is not kept.

   :param font: Font name (e.g. ``"slant"``) or a direct ``https://`` URL to an ``.flf`` file.
   :param target_dir: Directory to save the font into; defaults to the current directory.
   :raises UnreachableFigletFontException: the target directory is not writable.
   :raises InvalidFigletFontException: the name is invalid or the downloaded file is not a well-formed ``.flf``.
   :raises FigletFontFetchException: the font could not be downloaded from any source.
   :return: Path to the downloaded ``.flf`` file.

.. automethod:: argenta.app.presentation.ascii_art.FigletFontFetcher.list_available

   Returns the names of fonts available for download across the known collections, merged and sorted. Requires network access.

   :raises FigletFontFetchException: no collection could be reached.
   :return: List of font names.

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

.. autoexception:: argenta.app.presentation.ascii_art.FigletFontFetchException
   :show-inheritance:

   Raised by ``FigletFontFetcher`` when a font or the remote font index cannot be downloaded (unknown name, network failure, every source unreachable). The ``source`` attribute carries the requested font or index description.

-----

Usage Example
-------------

.. literalinclude:: ../../../code_snippets/ascii_art/snippet.py
   :language: python
   :linenos:
