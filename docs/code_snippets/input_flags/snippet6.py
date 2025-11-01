from argenta import Router, Command, Response
from argenta.command import Flag, Flags

router = Router(title="Index Access Example")

@router.command(Command(
    "example",
    description="Example with indexed access",
    flags=Flags([
        Flag("first"),
        Flag("second"),
        Flag("third")
    ])
))
def example_handler(response: Response):
    input_flags = response.input_flags
    
    # Получаем флаги по индексу
    if len(input_flags.flags) > 0:
        first_flag = input_flags[0]
        print(f"First flag: {first_flag.name} = {first_flag.input_value}")
    
    if len(input_flags.flags) > 1:
        second_flag = input_flags[1]
        print(f"Second flag: {second_flag.name} = {second_flag.input_value}")
    
    # Можно использовать срез для получения нескольких флагов
    if len(input_flags.flags) >= 2:
        first_two = input_flags.flags[:2]
        print(f"First two flags: {[f.name for f in first_two]}")

