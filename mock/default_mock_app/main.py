from argenta.app import App
from argenta.app.defaults import PredeterminedMessages


app = App(repeat_command_groups=True)

app.add_message_on_startup(PredeterminedMessages.USAGE + '\n\n')

app.start_polling()
