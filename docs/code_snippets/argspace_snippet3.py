from argenta import Response, Router
from argenta.di import FromDishka
from argenta.orchestrator.argparser import (ArgSpace, BooleanArgument,
                                            ValueArgument)

router = Router()

@router.command('get_args')
def get_args(response: Response, argspace: FromDishka[ArgSpace]):
    # Получение всех булевых флагов
    boolean_flags = argspace.get_by_type(BooleanArgument)
    print(f"Active flags: {[arg.name for arg in boolean_flags if arg.value]}")
    
    # Получение всех аргументов со значениями
    value_args = argspace.get_by_type(ValueArgument)
    for arg in value_args:
        print(f"{arg.name} = {arg.value}")
    
    # Подсчет количества аргументов каждого типа
    print(f"Boolean arguments: {len(argspace.get_by_type(BooleanArgument))}")
    print(f"Value arguments: {len(argspace.get_by_type(ValueArgument))}")