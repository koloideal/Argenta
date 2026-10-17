import re

from argenta import Command, Response, Router
from argenta.a2ui.catalog import _escape_pointer, build_surface
from argenta.a2ui.models import A2UIConfig, JsonValue, Message
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


def test_escape_pointer() -> None:
    assert _escape_pointer("a/b~c") == "a~1b~0c"


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


def test_log_card_bound_to_log_path() -> None:
    router = Router()
    router.command("a")(_handler)

    components, model = build_surface(_registered(router), A2UIConfig())

    log_text = _component_by_id(components, "a2ui_log_text")
    assert log_text["text"] == {"path": A2UIConfig().log_model_path}
    assert _component_by_id(components, "a2ui_log_card")["child"] == "a2ui_log_text"
    assert model["log"] == ""
    assert "a2ui_log_card" in _children(_component_by_id(components, "root"), "children")


def test_multiple_routers_get_separate_titles() -> None:
    first = Router(title="One")
    second = Router(title="Two")
    first.command("a")(_handler)
    second.command("b")(_handler)

    components, _ = build_surface(_registered(first, second), A2UIConfig())

    assert _string(_component_by_id(components, "router_title_0"), "text") == "One"
    assert _string(_component_by_id(components, "router_title_1"), "text") == "Two"
