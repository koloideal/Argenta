from argenta.command import Command, PredefinedFlags, Flags, Flag, PossibleValues
from argenta.response import Response
from argenta import Router


work_router: Router = Router(title="Work points:")

flag = Flag('csdv', possible_values=PossibleValues.NEITHER)


@work_router.command(
    Command("get",
        description="Get Help",
        aliases=["help", "Get_help"],
        flags=Flags([PredefinedFlags.PORT,
                     PredefinedFlags.HOST])))
def command_help(response: Response):
    print(response.status)
    print(response.input_flags.all_flags)


@work_router.command("run")
def command_start_solving(response: Response):
    print(response.status)
    print(response.input_flags.all_flags)
