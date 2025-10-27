from argenta import Router, Response
from argenta.di import FromDishka
from argenta.orchestrator.argparser import ArgSpace


router = Router()

@router.command('get_args')
async def get_args(response: Response, argspace: FromDishka[ArgSpace]):
    print(argspace.all_arguments)
    