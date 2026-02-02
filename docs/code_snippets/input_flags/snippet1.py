from argenta import Command, Response, Router
from argenta.command import Flag, Flags


router = Router(title="Example")

@router.command(
    Command(
        "example",
        description="Example command with flags",
        flags=Flags([Flag("name"), Flag("age")]),
    )
)
def example_handler(response: Response):
    input_flags = response.input_flags

    if input_flags:
        print(f"Received {len(input_flags)} flag(s)")
    else:
        print("No flags provided")
