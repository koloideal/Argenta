from argenta.a2ui.models import A2UIConfig, JsonValue, Message


class MessageFactory:
    """
    Private. Builds A2UI server-to-client messages bound
    to the configured surface and protocol version
    """

    def __init__(self, config: A2UIConfig) -> None:
        """
        :param config: surface and envelope configuration
        """
        self._config = config

    def create_surface(self) -> Message:
        """
        Private. Builds a createSurface message
        :return: message as dict
        """
        payload: Message = {"catalogId": self._config.catalog_id}
        if self._config.theme:
            payload["theme"] = self._config.theme
        return self._envelope("createSurface", payload)

    def update_components(self, components: list[Message]) -> Message:
        """
        Private. Builds an updateComponents message
        :param components: component definitions (adjacency list)
        :return: message as dict
        """
        return self._envelope("updateComponents", {"components": components})

    def update_data_model(self, path: str, new_value: JsonValue) -> Message:
        """
        Private. Builds an updateDataModel message
        :param path: JSON Pointer path inside the data model
        :param new_value: value written at the path
        :return: message as dict
        """
        return self._envelope("updateDataModel", {"path": path, "value": new_value})

    def delete_surface(self) -> Message:
        """
        Private. Builds a deleteSurface message
        :return: message as dict
        """
        return self._envelope("deleteSurface", {})

    def _envelope(self, kind: str, payload: Message) -> Message:
        body: Message = {"surfaceId": self._config.surface_id, **payload}
        return {"version": self._config.protocol_version, kind: body}


def extract_action(message: Message) -> Message | None:
    """
    Private. Extracts the action payload from a client-to-server message
    :param message: decoded client message
    :return: action payload or None if the message carries no valid action
    """
    action = message.get("action")
    if not isinstance(action, dict):
        return None
    if not isinstance(action.get("name"), str):
        return None
    return action
