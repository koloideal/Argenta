from argenta import Response, Router
from argenta.di import FromDishka
from argenta.orchestrator.argparser import ArgSpace, BooleanArgument, ValueArgument

router = Router()


@router.command("get_args")
def get_args(response: Response, argspace: FromDishka[ArgSpace]):
    # Get all boolean flags
    boolean_flags = argspace.get_by_type(BooleanArgument)
    print(f"Active flags: {[arg.name for arg in boolean_flags if arg.value]}")

    # Get all value arguments
    value_args = argspace.get_by_type(ValueArgument)
    for arg in value_args:
        print(f"{arg.name} = {arg.value}")

    # Count arguments of each type
    print(f"Boolean arguments: {len(argspace.get_by_type(BooleanArgument))}")
    print(f"Value arguments: {len(argspace.get_by_type(ValueArgument))}")
