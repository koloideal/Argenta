from argenta import Command, Response, Router
from argenta.command import Flag, Flags

router = Router(title="Bool Check Example")


@router.command(
    Command(
        "action",
        description="Action with optional flags",
        flags=Flags([Flag("option1"), Flag("option2")]),
    )
)
def action_handler(response: Response):
    input_flags = response.input_flags

    # Check for flags presence
    if input_flags:
        print("Flags were provided:")
        for flag in input_flags:
            print(f"  - {flag.name}: {flag.input_value}")
    else:
        print("No flags provided, using defaults")

    # Alternative way to check
    has_flags = bool(input_flags)
    print(f"\nHas flags: {has_flags}")
