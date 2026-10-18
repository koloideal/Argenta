# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import dataclasses
import os
import re
import typing
from datetime import datetime, timezone
from pathlib import Path

from sphinx.application import Sphinx

from argenta._doc import Doc

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


_QUALIFIED_NAME = re.compile(r"\b(?:[A-Za-z_]\w*\.)+([A-Za-z_]\w*)")


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


def _documented_fields(obj: object) -> list[tuple[dataclasses.Field[object], object, str]]:
    """Dataclass fields annotated as ``Annotated[type, Doc("...")]``"""
    if not (isinstance(obj, type) and dataclasses.is_dataclass(obj)):
        return []
    hints = typing.get_type_hints(obj, include_extras=True)
    documented = []
    for field in dataclasses.fields(obj):
        hint = hints[field.name]
        docs = [meta.text for meta in getattr(hint, "__metadata__", ()) if isinstance(meta, Doc)]
        if docs:
            documented.append((field, typing.get_args(hint)[0], docs[0]))
    return documented


def _type_name(hint: object) -> str:
    if isinstance(hint, type):
        return hint.__name__
    return _QUALIFIED_NAME.sub(r"\1", str(hint))


def document_config_fields(
    app: Sphinx,
    what: str,
    name: str,
    obj: object,
    options: dict[str, object],
    lines: list[str],
) -> None:
    """``Doc`` metadata of config fields becomes the parameter list of the class"""
    fields = _documented_fields(obj) if what == "class" else []
    if fields:
        lines.append("")
        lines.extend(f":param {field.name}: {text}" for field, _, text in fields)


def plain_config_signature(
    app: Sphinx,
    what: str,
    name: str,
    obj: object,
    options: dict[str, object],
    signature: str | None,
    return_annotation: str | None,
) -> tuple[str, str | None] | None:
    """Config signatures show the bare field types, not ``Annotated[..., Doc(...)]``"""
    fields = _documented_fields(obj) if what == "class" else []
    if not fields:
        return None
    params = ", ".join(
        f"{field.name}: {_type_name(hint)} = {field.default!r}" for field, hint, _ in fields
    )
    return f"({params})", None


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
    app.connect("autodoc-process-docstring", document_config_fields)
    # first non-None result wins: run before sphinx_autodoc_typehints (priority 500)
    app.connect("autodoc-process-signature", plain_config_signature, priority=100)

