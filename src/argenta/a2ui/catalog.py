from collections.abc import Iterable
from itertools import batched
from re import Pattern

from argenta.a2ui.config import A2UIConfig
from argenta.a2ui.models import JsonValue, Message
from argenta.app.registered_routers.entity import RegisteredRouters
from argenta.command.flag.models import Flag, PossibleValues
from argenta.router.entity import Router

type ContextBinding = dict[str, str]
type FlagDefaults = dict[str, bool | str | list[str]]
type SurfaceParts = tuple[list[Message], dict[str, JsonValue]]
type _ComponentList = list[Message]
type _IdList = list[str]


def _flag_path(trigger: str, flag_name: str) -> str:
    escaped_trigger = trigger.replace("~", "~0").replace("/", "~1")
    escaped_name = flag_name.replace("~", "~0").replace("/", "~1")
    return f"/forms/{escaped_trigger}/{escaped_name}"


def _path_binding(path: str) -> ContextBinding:
    return {"path": path}


def _component(component_id: str, kind: str, **properties: JsonValue) -> Message:
    return {"id": component_id, "component": kind, **properties}


def _flag_default(flag: Flag) -> bool | str | list[str]:
    """Private. Initial data model value matching the bound component:
    bool for CheckBox, string list for ChoicePicker, string otherwise"""
    if flag.possible_values is PossibleValues.NEITHER:
        return False
    if isinstance(flag.possible_values, Iterable) and not isinstance(
        flag.possible_values, (str, Pattern)
    ):
        return []
    return ""


class CatalogBuilder:
    """
    Private. Builds the surface component graph and initial data model
    from the registered routers: one card per command, one input per flag,
    plus a log list templated over the entries at the log data model path
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
        children: list[str] = [self._config.log_card_id]  # output first, commands below
        forms_model: dict[str, FlagDefaults] = {}

        for index, router in enumerate(registered_routers):
            components.extend(self._router_components(router, index, forms_model, children))
        components.extend(
            [
                _component(
                    self._config.log_entry_id,
                    self._config.text_component,
                    text=_path_binding("markdown"),  # scoped to the templated log entry
                ),
                _component(
                    self._config.log_list_id,
                    "List",
                    children={
                        "componentId": self._config.log_entry_id,
                        "path": self._config.log_model_path,
                    },
                ),
                _component(self._config.log_card_id, "Card", child=self._config.log_list_id),
                _component(self._config.surface_root_id, "Column", children=children),
            ]
        )
        return components, {"forms": forms_model, "log": []}

    def _router_components(
        self,
        router: Router,
        index: int,
        forms_model: dict[str, FlagDefaults],
        children: list[str],
    ) -> list[Message]:
        children.append(f"router_title_{index}")
        parts = [
            _component(
                f"router_title_{index}",
                self._config.text_component,
                text=router.title,
                variant="h4",
            )
        ]

        card_ids: list[str] = []
        for command_handler in router.command_handlers:
            command = command_handler.handled_command
            flags = list(command.registered_flags)
            forms_model[command.trigger] = {flag.name: _flag_default(flag) for flag in flags}
            card_ids.append(f"card_{command.trigger}")
            parts.extend(self._command_components(command.trigger, command.description, flags))
        self._card_rows(index, card_ids, children, parts)
        return parts

    def _card_rows(
        self,
        router_index: int,
        card_ids: _IdList,
        children: _IdList,
        parts: _ComponentList,
    ) -> None:
        """Private. Groups command cards into rows so commands
        do not stretch the full surface width"""
        for row_index, pair in enumerate(batched(card_ids, self._config.cards_per_row)):
            row_id = f"card_row_{router_index}_{row_index}"
            children.append(row_id)
            parts.append(_component(row_id, "Row", children=list(pair), justify="stretch"))

    def _command_components(
        self, trigger: str, description: str, flags: list[Flag]
    ) -> list[Message]:
        children = [f"desc_{trigger}"]
        action_context: dict[str, ContextBinding] = {}
        components = [
            _component(
                f"desc_{trigger}",
                self._config.text_component,
                text=description,
                variant="caption",
            )
        ]

        for flag in flags:
            field_id = f"field_{trigger}_{flag.name}"
            children.append(field_id)
            action_context[flag.name] = _path_binding(_flag_path(trigger, flag.name))
            components.append(self._field_component(field_id, flag, trigger))

        children.append(f"btn_{trigger}")
        components.extend(
            [
                _component(
                    f"btn_label_{trigger}",
                    self._config.text_component,
                    text=f"Run {trigger}",
                ),
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
        if isinstance(possible_values, Iterable) and not isinstance(
            possible_values, (str, Pattern)
        ):
            return self._picker(field_id, flag, path, possible_values)
        properties: dict[str, JsonValue] = {
            "label": flag.string_entity,
            "value": _path_binding(path),
        }
        if isinstance(possible_values, Pattern):
            properties["validationRegexp"] = possible_values.pattern
        return _component(field_id, "TextField", **properties)

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
