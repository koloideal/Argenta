from argenta import Command, Response, Router
from argenta.command import Flag, Flags
from argenta.command.flag import ValidationStatus

work_router: Router = Router(title="Base points:")


@work_router.command(
    Command(
        "hello",
        flags=Flags([
            Flag("test")
        ]),
        description="Hello, world!")
)
def command_help(response: Response):
    n = input('sfgdheth')
    print(f"Hello,{n} {response.input_flags.get_flag_by_name('test', with_status=ValidationStatus.VALID)}")
