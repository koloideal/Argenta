from argenta import App, Orchestrator
from argenta.app import PredefinedMessages, StaticDividingLine
from mock.mock_app.routers import work_router

def print_hello(entity: str):
    with open('hello.txt', 'a') as file:
        file.write(f'printer called: {entity}\n')
    print(entity)

app: App = App(
    dividing_line=StaticDividingLine(),
    override_system_messages=True,
    print_func=print_hello
)
orchestrator: Orchestrator = Orchestrator()


def main():
    app.include_router(work_router)

    app.add_message_on_startup(PredefinedMessages.USAGE)
    app.add_message_on_startup(PredefinedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredefinedMessages.HELP)

    orchestrator.start_polling(app)


if __name__ == "__main__":
    main()
    
    