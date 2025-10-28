from argenta import Router, Command, Response
from argenta.command import Flag, Flags

router = Router(title="Server Management")

@router.command(Command(
    "start",
    description="Start the server",
    flags=Flags([
        Flag("port", help="Server port", default="8080"),
        Flag("host", help="Server host", default="localhost"),
        Flag("debug", help="Enable debug mode")
    ]),
    aliases=["run"]
))
def handle_start(response: Response):
    input_flags = response.input_flags
    port_flag = input_flags.get_flag_by_name("port")
    host_flag = input_flags.get_flag_by_name("host")
    debug_flag = input_flags.get_flag_by_name("debug")
    
    host = host_flag.input_value if host_flag else "localhost"
    port = port_flag.input_value if port_flag else "8080"
    debug = debug_flag and debug_flag.input_value
    
    print(f"Starting server on {host}:{port}")
    if debug:
        print("Debug mode: ON")