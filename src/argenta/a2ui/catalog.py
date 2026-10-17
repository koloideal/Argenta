from collections.abc import Iterable
from re import Pattern

from argenta.a2ui.models import A2UIConfig, JsonValue, Message
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.command.flag.models import Flag, PossibleValues
from argenta.router.entity import Router

type ContextBinding = dict[str, str]
type FlagDefaults = dict[str, bool | str]
type SurfaceParts = tuple[list[Message], dict[str, JsonValue]]

_TEXT_KIND = "Text"


def _escape_pointer(segment: str) -> str:
    return segment.replace("~", "~0").replace("/", "~1")


def _flag_path(trigger: str, flag_name: str) -> str:
    return f"/forms/{_escape_pointer(trigger)}/{_escape_pointer(flag_name)}"


def _path_binding(path: str) -> ContextBinding:
    return {"path": path}


def _component(component_id: str, kind: str, **properties: JsonValue) -> Message:
    return {"id": component_id, "component": kind, **properties}


class CatalogBuilder:
    """
    Private. Builds the surface component graph and initial data model
    from the registered routers: one card per command, one input per flag,
    plus a log text component bound to the configured log data model path
    """

    def __init__(self, config: A2UIConfig) -> None:
        """
        :param config: surface configuration
        """
        self._config = config

    def build(self, registered_routers: RegisteredRouters) -> SurfaceParts:
        """
        Private. Emits the component list and initial data model
        :param registered_routers: routers registered in the app (system router included)
        :return: (components, initial_data_model)
        """
        components: list[Message] = []
        children: list[str] = []
        forms_model: dict[str, FlagDefaults] = {}

        for index, router in enumerate(registered_routers):
            components.extend(self._router_components(router, index, forms_model, children))

        children.append(self._config.log_card_id)
        components.extend(
            [
                _component(
                    self._config.log_text_id,
                    _TEXT_KIND,
                    text=_path_binding(self._config.log_model_path),
                ),
                _component(self._config.log_card_id, "Card", child=self._config.log_text_id),
                _component(self._config.surface_root_id, "Column", children=children),
            ]
        )
        return components, {"forms": forms_model, "log": ""}

    def _router_components(
        self,
        router: Router,
        index: int,
        forms_model: dict[str, FlagDefaults],
        children: list[str],
    ) -> list[Message]:
        title_id = f"router_title_{index}"
        children.append(title_id)
        parts = [_component(title_id, _TEXT_KIND, text=router.title, variant="h4")]

        for command_handler in router.command_handlers:
            command = command_handler.handled_command
            flags = list(command.registered_flags)
            forms_model[command.trigger] = {
                flag.name: (False if flag.possible_values is PossibleValues.NEITHER else "")
                for flag in flags
            }
            children.append(f"card_{command.trigger}")
            parts.extend(self._command_components(command.trigger, command.description, flags))
        return parts

    def _command_components(
        self, trigger: str, description: str, flags: list[Flag]
    ) -> list[Message]:
        children = [f"desc_{trigger}"]
        action_context: dict[str, ContextBinding] = {}
        components = [
            _component(f"desc_{trigger}", _TEXT_KIND, text=description, variant="caption")
        ]

        for flag in flags:
            field_id = f"field_{trigger}_{flag.name}"
            children.append(field_id)
            action_context[flag.name] = _path_binding(_flag_path(trigger, flag.name))
            components.append(self._field_component(field_id, flag, trigger))

        children.append(f"btn_{trigger}")
        components.extend(
            [
                _component(f"btn_label_{trigger}", _TEXT_KIND, text=f"Run {trigger}"),
                _component(
                    f"btn_{trigger}",
                    "Button",
                    child=f"btn_label_{trigger}",
                    variant="primary",
                    action={"event": {"name": trigger, "context": action_context}},
                ),
                _component(f"col_{trigger}", "Column", children=children),
                _component(f"card_{trigger}", "Card", child=f"col_{trigger}"),
            ]
        )
        return components

    def _field_component(self, field_id: str, flag: Flag, trigger: str) -> Message:
        path = _flag_path(trigger, flag.name)
        possible_values = flag.possible_values

        if possible_values is PossibleValues.NEITHER:
            return _component(
                field_id,
                "CheckBox",
                label=flag.string_entity,
                value=_path_binding(path),
            )
        if isinstance(possible_values, Pattern):
            return self._regex_field(field_id, flag, path, possible_values)
        if isinstance(possible_values, Iterable) and not isinstance(possible_values, str):
            return self._picker(field_id, flag, path, possible_values)
        return _component(
            field_id,
            "TextField",
            label=flag.string_entity,
            value=_path_binding(path),
        )

    def _regex_field(self, field_id: str, flag: Flag, path: str, pattern: Pattern[str]) -> Message:
        return _component(
            field_id,
            "TextField",
            label=flag.string_entity,
            value=_path_binding(path),
            checks=[
                {
                    "call": "regex",
                    "args": {"value": _path_binding(path), "pattern": pattern.pattern},
                    "message": f"Value must match {pattern.pattern}",
                }
            ],
        )

    def _picker(self, field_id: str, flag: Flag, path: str, options: Iterable[str]) -> Message:
        return _component(
            field_id,
            "ChoicePicker",
            variant="mutuallyExclusive",
            label=flag.string_entity,
            value=_path_binding(path),
            options=[{"label": option, "value": option} for option in sorted(options)],
        )


def build_surface(registered_routers: RegisteredRouters, config: A2UIConfig) -> SurfaceParts:
    """
    Private. Builds the surface components and initial data model
    from the registered routers
    :param registered_routers: routers registered in the app (system router included)
    :param config: surface configuration
    :return: (components, initial_data_model)
    """
    return CatalogBuilder(config).build(registered_routers)
