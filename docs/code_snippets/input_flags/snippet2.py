from argenta import Command, Response, Router
from argenta.command import Flag, Flags

router = Router(title="Get Flag Example")

@router.command(Command(
    "config",
    description="Configure settings",
    flags=Flags([
        Flag("host"),
        Flag("port"),
        Flag("debug")
    ])
))
def config_handler(response: Response):
    input_flags = response.input_flags
    
    # Получаем флаг по имени
    host_flag = input_flags.get_flag_by_name("host")
    port_flag = input_flags.get_flag_by_name("port")
    debug_flag = input_flags.get_flag_by_name("debug")
    
    if host_flag:
        print(f"Host: {host_flag.input_value}")
    
    if port_flag:
        print(f"Port: {port_flag.input_value}")
    
    if debug_flag:
        print("Debug mode enabled")
    
    # Если флаг не найден, get_flag_by_name вернёт None
    missing_flag = input_flags.get_flag_by_name("nonexistent")
    if missing_flag is None:
        print("Flag 'nonexistent' not found")

