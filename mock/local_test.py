from argenta import App, Command, Response, Router


app = App(override_system_messages=True)
router = Router()

@router.command(Command('command'))
def handler(_res: Response) -> None:
    pass

@router.command(Command('command_other'))
def handler2(_res: Response) -> None:
    pass

app.include_routers(router)
app._pre_cycle_setup()

assert app._most_similar_command('command_') == 'command'