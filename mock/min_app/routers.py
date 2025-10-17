# routers.py
from argenta import Router, Response, Command

router = Router(title="Quickstart Example")

@router.command(Command("hello", description="Say hello"))
def handler(response: Response):
    print("Hello, world!")
    