from argenta import Router, Response
from argenta.command import Command, Flag

router = Router()


@router.command(Command("greet", flags=Flag("name")))
def greet_handler(response: Response):
    # Get flag by name
    name_flag = response.input_flags.get_flag_by_name("name")

    # Check if flag was passed
    if name_flag:
        print(f"Hello, {name_flag.input_value}!")
    else:
        print("Hello, stranger!")
