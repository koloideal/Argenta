from argenta import Command, Response, Router, App, Orchestrator
from argenta.command import InputCommand

router = Router()
orchestrator = Orchestrator()

@router.command(Command('test'))
def test(_response: Response) -> None:  # pyright: ignore[reportUnusedFunction]
    print('test command')

app = App(override_system_messages=True, print_func=print)
app.include_router(router)
app.set_unknown_command_handler(lambda command: print(f'Unknown command: {command.trigger}'))
orchestrator.start_polling(app)