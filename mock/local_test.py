from argenta.app import App
from argenta.command import Command
from argenta.router import Router


router = Router()

@router.command(Command('test'))
def test():
    print(f'test command')

@router.command(Command('some'))
def test2():
    print(f'some command')

app = App()
app.include_router(router)
app.start_polling()