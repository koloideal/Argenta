from argenta import Router, Response, Command

work_router: Router = Router(title="Base points:")


@work_router.command(Command('hello', description="Hello, world!"))
def command_help(response: Response):
	print('Hello, world!')
