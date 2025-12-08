from argenta import Command, Response, Router
from argenta.command import InputCommand

router = Router()

@router.command(Command('heLLo'))
def handler(_res: Response) -> None:
    print("Hello World!")

router.finds_appropriate_handler(InputCommand('HellO'))
