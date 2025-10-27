from argenta import Orchestrator, App
from argenta.orchestrator.argparser import ArgParser, ValueArgument


# Определение аргументов приложения
arguments = [
    ValueArgument(
        "host",
        help="Server host",
        default="localhost"
    ),
    ValueArgument(
        "port",
        help="Server port",
        default="8080"
    ),
]

# Создание и запуск парсера
argparser = ArgParser(
    processed_args=arguments,
    name="WebServer",
    description="Simple web server"
)

app = App()
orchestrator = Orchestrator(argparser)


def main():
    # Получение аргументов только после инициализации Orchestrator
    argspace = argparser.parsed_argspace
    
    # Получение конкретных аргументов
    host = argspace.get_by_name("host")
    port = argspace.get_by_name("port")
    
    print("Server configuration:")
    print(f"  Host: {host.value}")
    print(f"  Port: {port.value}")
    
    orchestrator.start_polling(app)
    
if __name__ == "__main__":
    main()
    