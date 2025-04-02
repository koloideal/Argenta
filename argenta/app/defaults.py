from dataclasses import dataclass


@dataclass
class PredeterminedMessages:
    USAGE = '[b dim]Usage[/b dim]: [i]<command> <[green]flags[/green]>[/i]'
    HELP = '[b dim]Help[/b dim]: [i]<command>[/i] [b red]--help[/b red]'

