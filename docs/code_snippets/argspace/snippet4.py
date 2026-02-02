from argenta import Response, Router
from argenta.di import FromDishka
from argenta.orchestrator.argparser import ArgSpace

router = Router()


@router.command("get_args")
def get_args(response: Response, argspace: FromDishka[ArgSpace]):
    config_arg = argspace.get_by_name("config")
    if config_arg:
        print(f"Config path: {config_arg.value}")

    verbose_arg = argspace.get_by_name("verbose")
    if verbose_arg and verbose_arg.value:
        print("Verbose mode enabled")

    unknown_arg = argspace.get_by_name("nonexistent")
    if unknown_arg is None:
        print("Argument not found")
