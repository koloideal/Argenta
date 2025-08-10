from rich.console import Console

from argenta.command import Command, PredefinedFlags, Flags, Flag, PossibleValues
from argenta.response import Response
from argenta import Router


work_router: Router = Router(title="Work points:", disable_redirect_stdout=True)

console = Console()

flag = Flag('csdv', possible_values=PossibleValues.NEITHER)


@work_router.command(
    Command(
        "get",
        "Get Help",
        aliases=["help", "Get_help"],
        flags=Flags(PredefinedFlags.PORT, PredefinedFlags.HOST),
    )
)
def command_help(response: Response):
    case = input("test >  ")
    print(case)
    print(response.status)
    print(response.undefined_flags.get_flags())
    print(response.valid_flags.get_flags())
    print(response.invalid_value_flags.get_flags())


@work_router.command("run")
def command_start_solving(response: Response):
    print(response.status)
    print(response.undefined_flags.get_flags())
    print(response.valid_flags.get_flags())
    print(response.invalid_value_flags.get_flags())
