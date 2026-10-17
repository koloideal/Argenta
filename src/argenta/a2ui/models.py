from collections.abc import Mapping, Sequence
from dataclasses import dataclass

type JsonValue = bool | int | float | str | Sequence[JsonValue] | Mapping[str, JsonValue] | None
type Message = dict[str, JsonValue]


@dataclass(frozen=True)
class A2UIConfig:
    """
    Public. Configuration of the A2UI surface and the message envelope
    """

    protocol_version: str = "v0.9"
    catalog_id: str = "https://a2ui.org/specification/v0_9/catalogs/basic/catalog.json"
    surface_id: str = "main"
    surface_root_id: str = "root"
    log_card_id: str = "a2ui_log_card"
    log_text_id: str = "a2ui_log_text"
    log_model_path: str = "/log"
    max_log_lines: int = 500
    cards_per_row: int = 2
    text_component: str = "Text"
    theme: Mapping[str, JsonValue] | None = None
