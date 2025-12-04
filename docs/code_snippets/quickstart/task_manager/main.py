from argenta import App, Orchestrator

from .handlers import router
from .provider import TaskProvider

# 1. Create app and orchestrator instances
app = App(
    initial_message="Task Manager",
    prompt="Enter a command: ",
)
orchestrator = Orchestrator(custom_providers=[TaskProvider()])

# 2. Include router with our commands
app.include_router(router)

# 3. Start polling via orchestrator
if __name__ == "__main__":
    orchestrator.start_polling(app)
