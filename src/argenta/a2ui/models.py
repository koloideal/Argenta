from collections.abc import Mapping, Sequence

type JsonValue = bool | int | float | str | Sequence[JsonValue] | Mapping[str, JsonValue] | None
type Message = dict[str, JsonValue]
