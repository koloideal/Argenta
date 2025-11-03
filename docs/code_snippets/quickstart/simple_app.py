from argenta import App, Command, Orchestrator, Router, Response
from argenta.command import Flag

# 1. Создание экземпляра приложения и оркестратора
app = App(
    prompt=">> ",
    initial_message="Simple App",
    farewell_message="Goodbye!",
)
orchestrator = Orchestrator()

# 2. Создание роутера для группировки команд
main_router = Router(title="Основные команды")

# 3. Определение команды и её обработчика
@main_router.command(Command(
    "hello", 
    description="Печатает приветственное сообщение",
    flags=Flag("name")
))
def hello_handler(response: Response):
    """Этот обработчик будет вызван для команды 'hello'."""
    name = response.input_flags.get_flag_by_name("name")
    if name:
        print(f"Привет, {name.input_value}!")
    else:
        print("Привет, мир!")

# 4. Подключение роутера к приложению
app.include_router(main_router)

# 5. Запуск приложения
if __name__ == "__main__":
    orchestrator.start_polling(app)
