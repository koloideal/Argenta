from dataclasses import dataclass


@dataclass
class PredefinedMessages:
    """
    Public. A dataclass with predetermined messages for quick use
    """

    USAGE = "[b dim]Usage[/b dim]: [i]<command> <[green]flags[/green]>[/i]"
    HELP = "[b dim]Help[/b dim]: [i]<command>[/i] [b red]--help[/b red]"
    AUTOCOMPLETE = "[b dim]Autocomplete[/b dim]: [i]<part>[/i] [bold]<tab>"
