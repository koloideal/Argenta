from argenta import App


def empty_command_handler():
    print("Empty command handler called")

app: App = App()
app.set_empty_command_handler(empty_command_handler)
