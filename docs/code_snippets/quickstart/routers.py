# routers.py
from argenta import Command, Response, Router

router = Router(title="Quickstart Example")

@router.command(Command("hello", description="Say hello"))
def handler(response: Response):
    print("Hello, world!")
    