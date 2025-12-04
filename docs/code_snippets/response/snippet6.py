from argenta import Command, Response, Router
from argenta.command import Flag, Flags
from argenta.command.flag import ValidationStatus
from argenta.response import ResponseStatus

router = Router(title="Flags Example")


@router.command(
    Command(
        "process",
        description="Process with flags",
        flags=Flags([
            Flag("format", possible_values=["json", "xml"]), 
            Flag("verbose")
        ]),
    )
)
def process_handler(response: Response):
    print(f"Status: {response.status}")

    format_flag = response.input_flags.get_flag_by_name("format")
    verbose_flag = response.input_flags.get_flag_by_name("verbose")

    if format_flag:
        format_value = format_flag.input_value
        print(f"Format: {format_value}")

    if verbose_flag:
        print("Verbose mode enabled")

    if response.status == ResponseStatus.ALL_FLAGS_VALID:
        print("All flags are valid, proceeding...")
    elif response.status == ResponseStatus.INVALID_VALUE_FLAGS:
        print("Warning: Some flags have invalid values")
        for flag in response.input_flags:
            if flag.status == ValidationStatus.INVALID:
                print(f"  Invalid flag: {flag.string_entity} = {flag.input_value}")
