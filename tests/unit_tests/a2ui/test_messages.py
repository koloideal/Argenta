from argenta.a2ui.messages import MessageFactory, extract_action
from argenta.a2ui.models import A2UIConfig, Message

_CATALOG_URL = "https://a2ui.org/specification/v0_9/catalogs/basic/catalog.json"


def test_create_surface_defaults() -> None:
    message = MessageFactory(A2UIConfig()).create_surface()

    assert message == {
        "version": "v0.9",
        "createSurface": {"surfaceId": "main", "catalogId": _CATALOG_URL},
    }


def test_create_surface_with_theme() -> None:
    config = A2UIConfig(theme={"primaryColor": "#fff", "agentDisplayName": "Bot"})

    message = MessageFactory(config).create_surface()

    surface = message["createSurface"]
    assert isinstance(surface, dict)
    assert surface["theme"] == {"primaryColor": "#fff", "agentDisplayName": "Bot"}


def test_create_surface_custom_surface_and_catalog() -> None:
    config = A2UIConfig(surface_id="ui2", catalog_id="custom://catalog")

    message = MessageFactory(config).create_surface()

    assert message["createSurface"] == {
        "surfaceId": "ui2",
        "catalogId": "custom://catalog",
    }


def test_update_components() -> None:
    components: list[Message] = [{"id": "root", "component": "Column"}]

    message = MessageFactory(A2UIConfig()).update_components(components)

    assert message == {
        "version": "v0.9",
        "updateComponents": {"surfaceId": "main", "components": components},
    }


def test_update_data_model() -> None:
    message = MessageFactory(A2UIConfig()).update_data_model("/log", "line")

    assert message == {
        "version": "v0.9",
        "updateDataModel": {"surfaceId": "main", "path": "/log", "value": "line"},
    }


def test_delete_surface() -> None:
    message = MessageFactory(A2UIConfig()).delete_surface()

    assert message == {
        "version": "v0.9",
        "deleteSurface": {"surfaceId": "main"},
    }


def test_custom_protocol_version() -> None:
    config = A2UIConfig(protocol_version="v9.9")

    message = MessageFactory(config).delete_surface()

    assert message["version"] == "v9.9"


def test_extract_action_valid() -> None:
    action: Message = {"name": "deploy", "context": {"env": "prod"}}

    assert extract_action({"action": action}) is action


def test_extract_action_no_action_key() -> None:
    assert extract_action({"error": {"code": 1}}) is None


def test_extract_action_non_dict_action() -> None:
    assert extract_action({"action": "deploy"}) is None


def test_extract_action_missing_name() -> None:
    assert extract_action({"action": {"context": {}}}) is None


def test_extract_action_non_str_name() -> None:
    assert extract_action({"action": {"name": 42}}) is None
