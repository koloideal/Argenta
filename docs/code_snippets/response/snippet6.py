from argenta import Router, Command, Response
from argenta.command import Flag, Flags
from argenta.response import ResponseStatus

router = Router(title="Flags Example")

@router.command(Command(
    "process",
    description="Process with flags",
    flags=Flags([
        Flag("format", possible_values=["json", "xml"]),
        Flag("verbose")
    ])
))
def process_handler(response: Response):
    # Проверяем статус валидации флагов
    print(f"Status: {response.status.value}")
    
    # Работаем с флагами
    format_flag = response.input_flags.get_flag_by_name("format")
    verbose_flag = response.input_flags.get_flag_by_name("verbose")
    
    if format_flag:
        format_value = format_flag.input_value
        print(f"Format: {format_value}")
    
    if verbose_flag:
        print("Verbose mode enabled")
    
    # Проверяем валидность флагов
    if response.status == ResponseStatus.ALL_FLAGS_VALID:
        print("All flags are valid, proceeding...")
    elif response.status == ResponseStatus.INVALID_VALUE_FLAGS:
        print("Warning: Some flags have invalid values")
        for flag in response.input_flags:
            if flag.status and flag.status.name == "INVALID":
                print(f"  Invalid flag: {flag.string_entity} = {flag.input_value}")

