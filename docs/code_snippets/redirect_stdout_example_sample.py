from argenta.router import Router

# Для этого роутера перехват stdout будет отключен
interactive_router = Router(disable_redirect_stdout=True)

@interactive_router.command("ask")
def ask_name(response):
    name = input("Как вас зовут? ")
    print(f"Приятно познакомиться, {name}!")