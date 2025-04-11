from argenta.app import App
from argenta.command import Command
from argenta.router import Router

router = Router()

@router.command(Command('test'))
def test():
    print('test command')

app = App(ignore_command_register=False)
app.include_router(router)
app.set_unknown_command_handler(lambda command: print(f'Unknown command: {command.get_trigger()}'))
app.start_polling()