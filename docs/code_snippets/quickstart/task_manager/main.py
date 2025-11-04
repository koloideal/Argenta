from argenta import App, Orchestrator

from .handlers import router
from .provider import TaskProvider

# 1. Создаем экземпляр приложения и оркестратора
app = App(
    initial_message="Task Manager",
    prompt="Enter a command: ",
)
orchestrator = Orchestrator(custom_providers=[TaskProvider()])

# 2. Подключаем роутер с нашими командами
app.include_router(router)

# 3. Запускаем поллинг через оркестратор
if __name__ == "__main__":
    orchestrator.start_polling(app)
