from argenta import App


def incorrect_input_syntax_handler(raw_command: str):
    print(f"Incorrect input syntax for command: {raw_command}")


app: App = App()
app.set_incorrect_input_syntax_handler(incorrect_input_syntax_handler)
