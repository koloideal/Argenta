from argenta import Response, Router

# For this router stdout redirect will be disabled
interactive_router = Router(disable_redirect_stdout=True)


@interactive_router.command("ask")
def ask_name(response: Response):
    name = input("What is your name? ")
    print(f"Nice to meet you, {name}!")
