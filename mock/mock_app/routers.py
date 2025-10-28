from dishka import FromDishka

from argenta import Router
from argenta.command import Flag, PossibleValues
from argenta.orchestrator.argparser import ArgSpace
from argenta.response import Response
from argenta.router.defaults import system_router

work_router: Router = Router(title="Work points:")

flag = Flag("csdv", possible_values=PossibleValues.NEITHER)


@work_router.command("get")
def command_help(response: Response, argspace: FromDishka[ArgSpace]):
	print(argspace.all_arguments)


@system_router.command("run")
def command_start_solving(response: Response):
    print(response.get_data())
