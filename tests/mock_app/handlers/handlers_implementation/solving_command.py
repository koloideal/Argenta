from rich.console import Console
from ...business_logic.word2num_math import word2num_math


console = Console()
print_line_separator = lambda: console.print('\n[bold blue]--------------------------------------[/bold blue]\n')


def start_solving_command():
    while True:
        console.print(
            "\n[italic]Enter a string expression or [bold italic green] Q [/bold italic green] for exit:[/italic]")
        string_expression = input()
        if string_expression.lower() == 'q':
            break
        else:
            print_line_separator()
            console.print(
                f'[bold green]Answer:[/bold green]  [bold blue]{word2num_math(string_expression)}[/bold blue]')
            print_line_separator()
