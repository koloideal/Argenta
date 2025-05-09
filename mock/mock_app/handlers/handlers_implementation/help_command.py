from rich.console import Console


console = Console()


def help_command():
    console.print(
        "[italic bold]The main functionality of the script is to convert an expression from a string "
        "to a mathematical one and then calculate this expression. "
        "Project GitHub: https://github.com/koloideal/WordMath[/italic bold]"
    )
