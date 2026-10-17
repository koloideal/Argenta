from argenta.app import App
from argenta.command.exceptions import InputCommandException
from argenta.command.models import InputCommand


class REPLRuntime:
    """
    Public. Runs an App as an interactive REPL: prompts for commands,
    parses the raw input and routes it through the regular command
    dispatch path
    """

    def __init__(self, app: App) -> None:
        """
        :param app: the application to run interactively
        """
        self._app = app

    def run(self) -> None:
        """
        Public. Prints the initial message, performs the app setup,
        prepares the autocompleter and enters the read-eval-print loop
        :return: None
        """
        app = self._app
        app.viewer.view_initial_message(app.initial_message)
        app.prepare_for_run()
        app.autocompleter.initial_setup(app.registered_routers.get_triggers())
        while True:
            if app.repeat_command_groups_printing:
                app.viewer.view_command_groups_description(
                    app.description_message_generator, app.registered_routers
                )

            raw_command = self._read_command()
            if raw_command is not None and self._dispatch_command(raw_command):
                return

    def _read_command(self) -> str | None:
        try:
            return self._prompt_for_command()
        except KeyboardInterrupt:
            return None
        except EOFError:
            return self._app.exit_command.trigger

    def _prompt_for_command(self) -> str:
        self._app.printer("")  # pre-prompt gap
        raw_command: str = self._app.autocompleter.prompt(
            self._app.renderer.render_prompt(self._app.prompt)
        )
        self._app.printer("")  # post-prompt gap
        return raw_command

    def _dispatch_command(self, raw_command: str) -> bool:
        try:
            input_command = InputCommand.parse(raw_command=raw_command)
        except InputCommandException as error:
            self._app.handle_input_error(error, raw_command)
            return False

        return self._app.dispatch_input_command(input_command)
