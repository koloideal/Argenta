from argenta import Response, Router
from argenta.orchestrator.argparser import ArgSpace
from argenta.di import FromDishka


router = Router()

@router.command('info')
def connect_handler(response: Response, argspace: FromDishka[ArgSpace]):
	print(argspace.get_by_name('type'))
	