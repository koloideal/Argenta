from argenta import Command, Response, Router
from argenta.command import Flag, Flags
from argenta.command.flag import InputFlag

router = Router(title="Contains Example")

@router.command(Command(
    "check",
    description="Check flags",
    flags=Flags([
        Flag("verbose"),
        Flag("debug"),
        Flag("quiet")
    ])
))
def check_handler(response: Response):
    input_flags = response.input_flags
    
    # Проверяем наличие конкретного флага
    verbose_flag = input_flags.get_flag_by_name("verbose")
    debug_flag = input_flags.get_flag_by_name("debug")
    
    # Используем оператор in для проверки
    if verbose_flag and verbose_flag in input_flags:
        print("Verbose flag is present")
    
    if debug_flag and debug_flag in input_flags:
        print("Debug flag is present")
    
    # Можно создать флаг для проверки (сравнение идёт по имени)
    test_flag = InputFlag(
        name="verbose",
        prefix="--",
        input_value="any",
        status=None
    )
    
    if test_flag in input_flags:
        print("Verbose flag found using 'in' operator")

