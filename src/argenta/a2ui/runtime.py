import traceback
from collections.abc import Callable
from contextlib import redirect_stdout
from io import StringIO

from argenta.a2ui.catalog import build_surface
from argenta.a2ui.messages import MessageFactory, extract_action
from argenta.a2ui.models import A2UIConfig, JsonValue, Message
from argenta.a2ui.transport import Transport
from argenta.app import App
from argenta.command import Command, InputCommand, InputFlags
from argenta.command.flag.models import Flag, InputFlag, PossibleValues


def _to_input_flag(flag: Flag, flag_value: JsonValue) -> InputFlag:
    raw_value = "" if flag.possible_values is PossibleValues.NEITHER else str(flag_value)
    return InputFlag(name=flag.name, input_value=raw_value, prefix=flag.prefix)


def _find_command(app: App, trigger: str) -> Command | None:
    router = app.registered_routers.get_router_by_trigger(trigger.lower())
    if router is None:
        return None
    command_handler = router.command_handlers.get_command_handler_by_trigger(trigger.lower())
    if command_handler is None:
        return None
    return command_handler.handled_command


class AgentRuntime:
    """
    Public. Runs an App as an A2UI agent: emits a surface built from the
    registered commands and routes incoming actions through the regular
    command dispatch path
    """

    def __init__(self, app: App, transport: Transport, config: A2UIConfig | None = None) -> None:
        """
        :param app: the application to expose as an A2UI agent
        :param transport: message transport
        :param config: surface and envelope configuration
        """
        self._app = app
        self._transport = transport
        self._config = config or A2UIConfig()
        self._messages = MessageFactory(self._config)
        self._log_lines: list[str] = []
        self._log_dirty = False

    def run(self) -> None:
        """
        Public. Emits the surface and enters the action dispatch loop
        :return: None
        """
        self._capture_into_log(self._app.prepare_for_run)

        components, data_model = build_surface(self._app.registered_routers, self._config)
        self._transport.send(self._messages.create_surface())
        self._transport.send(self._messages.update_components(components))
        self._transport.send(self._messages.update_data_model("/", data_model))
        self._flush_log()

        for message in self._transport.actions():
            action = extract_action(message)
            if action is not None and self._dispatch_action(action):
                break
        self._transport.send(self._messages.delete_surface())

    def _capture_into_log[ResultT](self, func: Callable[[], ResultT]) -> ResultT:
        buffer = StringIO()
        with redirect_stdout(buffer):
            func_result = func()
        output = buffer.getvalue().strip("\n")
        if output:
            max_lines = self._config.max_log_lines
            self._log_lines.extend(output.split("\n"))
            self._log_lines = self._log_lines[-max_lines:]
            self._log_dirty = True
        return func_result

    def _flush_log(self) -> None:
        if self._log_dirty:
            self._transport.send(
                self._messages.update_data_model(
                    self._config.log_model_path, "\n".join(self._log_lines)
                )
            )
            self._log_dirty = False

    def _dispatch_action(self, action: Message) -> bool:
        input_command = self._build_input_command(action)
        try:
            is_exit = self._capture_into_log(
                lambda: self._app.dispatch_input_command(input_command)
            )
        except Exception:  # noqa: BLE001
            self._log_lines.extend(traceback.format_exc().splitlines())
            is_exit = False
        self._flush_log()
        return is_exit

    def _build_input_command(self, action: Message) -> InputCommand:
        trigger = str(action["name"])
        context = action.get("context")
        command = _find_command(self._app, trigger)

        if command is not None and isinstance(context, dict):
            return InputCommand(trigger=trigger, input_flags=self._context_flags(command, context))
        return InputCommand(trigger=trigger, input_flags=InputFlags())

    def _context_flags(self, command: Command, context: Message) -> InputFlags:
        input_flags = InputFlags()
        for flag in command.registered_flags:
            flag_value = context.get(flag.name)
            if flag_value and not isinstance(flag_value, dict):
                input_flags.add_flag(_to_input_flag(flag, flag_value))
        return input_flags
