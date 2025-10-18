from sqlite3 import Connection

from argenta import Response, Router
from argenta.di import FromDishka


router = Router()

@router.command('connect')
def connect_handler(response: Response, connection: FromDishka[Connection]):
	connection.execute('...')
	