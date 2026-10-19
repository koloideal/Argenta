from collections.abc import Mapping
from dataclasses import dataclass
from typing import Annotated

from argenta.a2ui.models import JsonValue


@dataclass(frozen=True)
class A2UIConfig:
    """
    Public. Configuration of the A2UI surface and the message envelope
    """

    protocol_version: Annotated[
        str, "A2UI protocol version written into the `version` field of every message"
    ] = "v0.9"
    catalog_id: Annotated[
        str,
        "Component catalog the surface declares in createSurface; the renderer must know it",
    ] = "https://a2ui.org/specification/v0_9/catalogs/basic/catalog.json"
    surface_id: Annotated[str, "Id of the surface every message targets (`surfaceId`)"] = "main"
    surface_root_id: Annotated[
        str, "Id of the root Column holding the log card and the command cards"
    ] = "root"
    log_card_id: Annotated[
        str, "Id of the Card wrapping the output log; the first child of the root"
    ] = "a2ui_log_card"
    log_list_id: Annotated[
        str, "Id of the List inside the log card, templated over the log entries"
    ] = "a2ui_log_list"
    log_entry_id: Annotated[
        str, "Id of the Text template the List instantiates once per log entry"
    ] = "a2ui_log_entry"
    log_model_path: Annotated[
        str, "Data model path holding the list of log entries ({id, kind, text, markdown})"
    ] = "/log"
    log_fence: Annotated[
        str,
        (
            "Markdown code fence around each entry's `markdown` so renderers keep monospace "
            "layout; four backticks let handler output contain ``` itself"
        ),
    ] = "````"
    max_log_entries: Annotated[
        int, "How many log entries are kept and resent; the oldest are dropped first"
    ] = 200
    cards_per_row: Annotated[int, "How many command cards share one row of the surface"] = 2
    text_component: Annotated[
        str, "Catalog component used for text: router titles, descriptions, log entries"
    ] = "Text"
    theme: Annotated[
        Mapping[str, JsonValue] | None,
        "Optional theme sent in createSurface (colors, fonts); renderer-specific keys",
    ] = None
