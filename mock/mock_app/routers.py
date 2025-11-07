from argenta import Router, Response, Command

work_router: Router = Router(title="Base points:", disable_redirect_stdout=True)


@work_router.command(Command('hello', description="Hello, world!"))
def command_help(response: Response):
	c = input("Enter your name: ")
	print(f"Hello, {c}!")
