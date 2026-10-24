import re

from argenta import Command, Response, Router
from argenta.a2ui.catalog import _flag_path, build_surface
from argenta.a2ui.config import A2UIConfig
from argenta.a2ui.models import JsonValue, Message
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.command.flag import Flag, Flags, PossibleValues


def _registered(*routers: Router) -> RegisteredRouters:
    registered = RegisteredRouters()
    for router in routers:
        registered.add_registered_router(router)
    return registered


def _handler(_response: Response) -> None:
    pass


def _component_by_id(components: list[Message], component_id: str) -> Message:
    return next(component for component in components if component.get("id") == component_id)


def _string(component: Message, key: str) -> str:
    value = component[key]
    assert isinstance(value, str)
    return value


def _section(component: Message, key: str) -> Message:
    value = component[key]
    assert isinstance(value, dict)
    return value


def _children(component: Message, key: str) -> list[JsonValue]:
    value = component[key]
    assert isinstance(value, list)
    return value


def test_flag_path_escapes_segments() -> None:
    assert _flag_path("a/b", "c~d") == "/forms/a~1b/c~0d"


def test_router_titles() -> None:
    router = Router(title="My Router")
    router.command("a")(_handler)
    router.command("b")(_handler)

    components, _ = build_surface(_registered(router), A2UIConfig())

    assert _string(_component_by_id(components, "router_title_0"), "text") == "My Router"
    assert "router_title_0" in _children(_component_by_id(components, "root"), "children")


def test_command_card_structure() -> None:
    router = Router()
    router.command(Command("deploy", description="Deploy it", aliases={"dep"}))(_handler)

    components, _ = build_surface(_registered(router), A2UIConfig())

    card = _component_by_id(components, "card_deploy")
    column = _component_by_id(components, _string(card, "child"))
    children = _children(column, "children")
    assert "desc_deploy" in children
    assert "btn_deploy" in children
    assert _string(_component_by_id(components, "desc_deploy"), "text") == "Deploy it"

    button = _component_by_id(components, "btn_deploy")
    event = _section(_section(button, "action"), "event")
    assert event["name"] == "deploy"


def test_no_flags_command_model() -> None:
    router = Router()
    router.command("bare")(_handler)

    _, model = build_surface(_registered(router), A2UIConfig())
    forms = model["forms"]

    assert isinstance(forms, dict)
    assert forms["bare"] == {}


def test_checkbox_for_neither_flag() -> None:
    router = Router()
    router.command(Command("c", flags=Flags([Flag("f", possible_values=PossibleValues.NEITHER)])))(
        _handler
    )

    components, model = build_surface(_registered(router), A2UIConfig())

    field = _component_by_id(components, "field_c_f")
    assert field["component"] == "CheckBox"
    assert field["label"] == "--f"
    assert field["value"] == {"path": "/forms/c/f"}
    forms = model["forms"]
    assert isinstance(forms, dict)
    assert forms["c"] == {"f": False}


def test_text_field_with_regex_check() -> None:
    router = Router()
    router.command(Command("c", flags=Flags([Flag("n", possible_values=re.compile(r"^\d+$"))])))(
        _handler
    )

    components, _ = build_surface(_registered(router), A2UIConfig())

    field = _component_by_id(components, "field_c_n")
    assert field["component"] == "TextField"
    assert field["validationRegexp"] == r"^\d+$"


def test_choice_picker_for_list_values() -> None:
    router = Router()
    router.command(Command("c", flags=Flags([Flag("env", possible_values=["prod", "dev"])])))(
        _handler
    )

    components, model = build_surface(_registered(router), A2UIConfig())

    field = _component_by_id(components, "field_c_env")
    assert field["component"] == "ChoicePicker"
    assert field["variant"] == "mutuallyExclusive"
    assert field["options"] == [
        {"label": "dev", "value": "dev"},
        {"label": "prod", "value": "prod"},
    ]
    forms = model["forms"]
    assert isinstance(forms, dict)
    assert forms["c"] == {"env": []}


def test_plain_text_field_for_all_and_str_values() -> None:
    router = Router()
    router.command(
        Command(
            "c",
            flags=Flags(
                [
                    Flag("a", possible_values=PossibleValues.ALL),
                    Flag("b", possible_values="literal"),
                ]
            ),
        )
    )(_handler)

    components, _ = build_surface(_registered(router), A2UIConfig())

    field_a = _component_by_id(components, "field_c_a")
    assert field_a["component"] == "TextField"
    assert "validationRegexp" not in field_a
    assert _component_by_id(components, "field_c_b")["component"] == "TextField"


def test_action_context_binds_flag_paths() -> None:
    router = Router()
    router.command(
        Command(
            "c",
            flags=Flags(
                [
                    Flag("env", possible_values=["x"]),
                    Flag("f", possible_values=PossibleValues.NEITHER),
                ]
            ),
        )
    )(_handler)

    components, _ = build_surface(_registered(router), A2UIConfig())

    button = _component_by_id(components, "btn_c")
    event = _section(_section(button, "action"), "event")
    assert event["context"] == {
        "env": {"path": "/forms/c/env"},
        "f": {"path": "/forms/c/f"},
    }


def test_log_card_lists_entries_from_log_path() -> None:
    router = Router()
    router.command("a")(_handler)

    components, model = build_surface(_registered(router), A2UIConfig())

    log_list = _component_by_id(components, "a2ui_log_list")
    assert log_list["component"] == "List"
    assert log_list["children"] == {
        "componentId": "a2ui_log_entry",
        "path": A2UIConfig().log_model_path,
    }
    assert _component_by_id(components, "a2ui_log_entry")["text"] == {"path": "markdown"}
    assert _component_by_id(components, "a2ui_log_card")["child"] == "a2ui_log_list"
    assert model["log"] == []
    assert _children(_component_by_id(components, "root"), "children")[0] == "a2ui_log_card"


def test_command_cards_pair_into_rows() -> None:
    router = Router()
    router.command("alpha")(_handler)
    router.command("beta")(_handler)
    router.command("gamma")(_handler)

    components, _ = build_surface(_registered(router), A2UIConfig())

    root_children = _children(_component_by_id(components, "root"), "children")
    assert "card_alpha" not in root_children
    first_row = _component_by_id(components, "card_row_0_0")
    second_row = _component_by_id(components, "card_row_0_1")
    assert first_row["component"] == "Row"
    assert _children(first_row, "children") == ["card_alpha", "card_beta"]
    assert _children(second_row, "children") == ["card_gamma"]
    assert root_children == ["a2ui_log_card", "router_title_0", "card_row_0_0", "card_row_0_1"]


def test_cards_per_row_is_configurable() -> None:
    router = Router()
    router.command("alpha")(_handler)
    router.command("beta")(_handler)
    router.command("gamma")(_handler)

    components, _ = build_surface(_registered(router), A2UIConfig(cards_per_row=3))

    first_row = _component_by_id(components, "card_row_0_0")
    assert _children(first_row, "children") == ["card_alpha", "card_beta", "card_gamma"]


def test_multiple_routers_get_separate_titles() -> None:
    first = Router(title="One")
    second = Router(title="Two")
    first.command("a")(_handler)
    second.command("b")(_handler)

    components, _ = build_surface(_registered(first, second), A2UIConfig())

    assert _string(_component_by_id(components, "router_title_0"), "text") == "One"
    assert _string(_component_by_id(components, "router_title_1"), "text") == "Two"
