from argenta.app import App
from argenta.command.models import InputCommand

app = App()
app._all_registered_triggers_in_lower = ['fr', 'Tre', 'Pre']
print(app._is_unknown_command(InputCommand('fr')))