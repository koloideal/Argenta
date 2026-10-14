# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
from datetime import datetime, timezone
from pathlib import Path

from sphinx.application import Sphinx

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Argenta"
copyright = f"2025–{datetime.now(timezone.utc).year}, kolo"
author = "kolo"
root_doc = "index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

extensions = [
    "sphinx_sitemap",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
]
sitemap_url_scheme = "{link}"

# -- Options for autodoc -----------------------------------------------------

autodoc_member_order = "bysource"
autodoc_preserve_defaults = True
autodoc_inherit_docstrings = False
add_module_names = False
typehints_use_signature = True
typehints_use_signature_return = True

_VISIBILITY_MARKER = re.compile(r"^(?:Public|Private)\.\s+")


def strip_visibility_markers(
    app: Sphinx,
    what: str,
    name: str,
    obj: object,
    options: dict[str, object],
    lines: list[str],
) -> None:
    if lines:
        lines[0] = _VISIBILITY_MARKER.sub("", lines[0])


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "shibuya"
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "https://argenta.wiki/")

html_theme_options = {
  "accent_color": "cyan",
  "nav_links": [
         {
             "title": "Sponsor me",
             "url": "https://github.com/sponsors/koloideal"
         },
     ],
    "github_url": "https://github.com/koloideal/Argenta",
    "linkedin_url": "https://www.linkedin.com/in/dmitry-shevelev-31b9a6324"
}


def render_base_url_files(app: Sphinx, exception: Exception | None) -> None:
    if exception is not None or app.builder.format != "html":
        return
    for name in ("robots.txt", "llms.txt"):
        template = Path(app.confdir, name).read_text(encoding="utf-8")
        Path(app.outdir, name).write_text(
            template.replace("{base_url}", html_baseurl), encoding="utf-8"
        )


def setup(app: Sphinx) -> None:
    app.connect("build-finished", render_base_url_files)
    app.connect("autodoc-process-docstring", strip_visibility_markers)

