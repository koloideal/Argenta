from argenta import App

def repeated_input_flags_handler(raw_command: str):
    print(f"Repeated input flags: {raw_command}")

app: App = App()
app.set_repeated_input_flags_handler(repeated_input_flags_handler)
