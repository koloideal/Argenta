from argenta.command import Command, PredefinedFlags, Flags, Flag, PossibleValues
from argenta.response import Response
from argenta import Router
from argenta.router.defaults import system_router


work_router: Router = Router(title="Work points:", disable_redirect_stdout=True)

flag = Flag("csdv", possible_values=PossibleValues.NEITHER)


@work_router.command(
    Command(
        "get",
        description="Get Help",
        aliases=["help", "Get_help"],
        flags=Flags([PredefinedFlags.PORT, PredefinedFlags.HOST]),
    )
)
def command_help(response: Response):
	response.update_data({"data": [_ for _ in range(9999999)]})


@system_router.command("run")
def command_start_solving(response: Response):
    print(response.get_data())
