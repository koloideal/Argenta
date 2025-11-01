from argenta import App
from argenta.command import InputCommand


def unknown_command_handler(command: InputCommand):
    print(f"Unknown input command with trigger: {command.trigger}")


app: App = App()
app.set_unknown_command_handler(unknown_command_handler)
