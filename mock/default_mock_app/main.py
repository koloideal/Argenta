from argenta.app import App
from argenta.orchestrator import Orchestrator

app = App(repeat_command_groups=True)

orchestrator = Orchestrator()
orchestrator.start_polling(app)
