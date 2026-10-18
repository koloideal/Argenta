from argenta import App, Response


def exit_command_handler(response: Response):
    print("Exit command handler")


app: App = App()
app.set_exit_command_handler(exit_command_handler)
