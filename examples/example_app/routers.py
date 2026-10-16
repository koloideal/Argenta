from argenta import Command, Response, Router
from argenta.command import Flag
from argenta.command.flag import ValidationStatus

work_router: Router = Router(title="Base points:")


@work_router.command(Command("greet", flags=Flag("name"), description="Greet the user by name"))
def greet_handler(response: Response) -> None:
    name_flag = response.input_flags.get_flag_by_name("name", with_status=ValidationStatus.VALID)
    if name_flag:
        print(f"Hello, {name_flag.input_value}!")
    else:
        print("Hello, world!")
