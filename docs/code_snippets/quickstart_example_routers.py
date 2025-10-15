# routers.py
from argenta import Router, Response

router = Router()

@router.command("hello")
def handler(response: Response):
    print("Hello, world!")
    