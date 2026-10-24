from argenta.app import App
from argenta.command.exceptions import InputCommandException
from argenta.command.models import InputCommand
from argenta.repl.config import REPLConfig
from argenta.repl.layout import TerminalLayout


class REPLRuntime:
    """
    Public. Runs an App as an interactive REPL: prompts for commands,
    parses the raw input and routes it through the regular command
    dispatch path; output is laid out by the terminal layout
    """

    def __init__(self, app: App, config: REPLConfig | None = None) -> None:
        """
        :param app: the application to run interactively
        :param config: terminal layout configuration
        """
        self._app = app
        self._layout = TerminalLayout(app.printer, app.renderer, config or REPLConfig())

    def run(self) -> None:
        """
        Public. Presents the startup blocks, prepares the autocompleter
        and enters the read-eval-print loop
        :return: None
        """
        app = self._app
        app.prepare_for_run(self._layout)
        app.autocompleter.initial_setup(app.registered_routers.get_triggers())
        while True:
            if app.repeat_command_groups_printing:
                app.present_command_groups(self._layout)

            raw_command = self._read_command()
            if raw_command is not None and self._dispatch_command(raw_command):
                return

    def _read_command(self) -> str | None:
        try:
            return self._layout.read_input(self._prompt_for_command)
        except KeyboardInterrupt:
            return None
        except EOFError:
            return self._app.exit_command.trigger

    def _prompt_for_command(self) -> str:
        return self._app.autocompleter.prompt(self._app.renderer.render_prompt(self._app.prompt))

    def _dispatch_command(self, raw_command: str) -> bool:
        try:
            input_command = InputCommand.parse(raw_command=raw_command)
        except InputCommandException as error:
            self._app.handle_input_error(error, raw_command, self._layout)
            return False

        return self._app.dispatch_input_command(input_command, self._layout)
