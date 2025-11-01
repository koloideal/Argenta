from argenta import App, Orchestrator

from .handlers import router
from .provider import TaskProvider

# 1. Создаем экземпляр приложения
app = App(
    initial_message="Task Manager",
    prompt="Enter a command: ",
)

# 2. Подключаем роутер с нашими командами
app.include_router(router)

# 3. Создаем и запускаем оркестратор
if __name__ == "__main__":
    orchestrator = Orchestrator(custom_providers=[TaskProvider()])
    orchestrator.start_polling(app)
