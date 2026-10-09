from typing import Any


class DataBridge:
    def __init__(self, initial_data: dict[str, Any] | None = None) -> None:
        self._storage: dict[str, Any] = initial_data if initial_data else {}

    def update(self, new_data: dict[str, Any]) -> None:
        self._storage.update(new_data)

    def get_all(self) -> dict[str, Any]:
        return self._storage

    def clear_all(self) -> None:
        self._storage.clear()

    def get_by_key(self, key: str) -> Any:
        return self._storage.get(key)

    def delete_by_key(self, key: str) -> None:
        self._storage.pop(key)
