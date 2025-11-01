from argenta import App


def custom_print_function(text: str) -> None:
    """Простая пользовательская функция вывода с префиксом."""
    print(f"Префикс: {text}")


app = App(
    initial_message="My App",
    override_system_messages=True,
    print_func=custom_print_function,
)
