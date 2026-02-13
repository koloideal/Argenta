from argenta import App, Command, Response, Router, Orchestrator

app = App(override_system_messages=True)
router = Router()

@router.command(Command('command'))
def handler(_res: Response) -> None:
    pass

@router.command(Command('command_other'))
def handler2(_res: Response) -> None:
    pass

orch = Orchestrator()