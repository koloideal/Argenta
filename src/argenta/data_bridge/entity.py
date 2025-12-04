__all__ = ["DataBridge"]

from typing import Any


class DataBridge:
    def __init__(self, initial_data: dict[str, Any] | None = None) -> None:
        self._data: dict[str, Any] = initial_data if initial_data else {}

    def update(self, data: dict[str, Any]) -> None:
        self._data.update(data)

    def get_all(self) -> dict[str, Any]:
        return self._data

    def clear_all(self) -> None:
        self._data.clear()

    def get_by_key(self, key: str) -> Any:
        return self._data.get(key)

    def delete_by_key(self, key: str) -> None:
        self._data.pop(key)
