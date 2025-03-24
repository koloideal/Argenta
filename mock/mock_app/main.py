from mock.mock_app.handlers.routers import work_router, settings_router
from art import text2art
from rich.console import Console

from argenta.app import App

app: App = App(prompt='[italic white bold]What do you want to do(enter number of action)?',
               line_separate=f'\n{"[bold green]-[/bold green][bold red]-[/bold red]"*25}\n',
               print_func=Console().print,
               command_group_description_separate='',
               repeat_command_groups=True,
               ignore_exit_command_register=False)


def main():
    ascii_name: str = text2art('WordMath', font='nancyj')
    initial_greeting: str = f'[bold red]\n\n{ascii_name}'

    ascii_goodbye_message: str = text2art('GoodBye', font='small')
    goodbye_message: str = f'[bold red]\n{ascii_goodbye_message}{' '*12}made by kolo\n'

    app.include_router(work_router)
    app.include_router(settings_router)

    app.set_initial_message(initial_greeting)
    app.set_farewell_message(goodbye_message)

    app.add_message_on_startup('--help for get helping\n\n')

    app.set_invalid_input_flags_handler(lambda raw_command: print(f"Invalid input flags: {raw_command}"))
    app.set_unknown_command_handler(lambda command: print(f"Unknown command: {command.get_trigger()}"))
    app.set_repeated_input_flags_handler(lambda raw_command: print(f"Repeated input flags: {raw_command}"))

    app.set_description_message_pattern('[bold red][{command}][/bold red] [blue]*=*=*[/blue] [bold yellow italic]{description}')

    app.start_polling()

if __name__ == "__main__":
    main()
