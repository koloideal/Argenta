from rich.console import Console
from rich.markup import escape


console = Console()
text = lambda command, description: f'[bold red]{escape('['+command+']')}[/bold red] [blue dim]*=*=*[/blue dim] [bold yellow italic]{escape(description)}'
print(text('start', 'command start'))
console.print(text('start', 'command start'))
