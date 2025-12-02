from argenta import Command, Response, Router
from argenta.command import Flag, Flags, InputFlag
from argenta.command.flag import ValidationStatus

router = Router(title="Comprehensive Example")


@router.command(
    Command(
        "validate",
        description="Validate all flags",
        flags=Flags(
            [
                Flag("format", possible_values=["json", "xml"]),
                Flag("output"),
                Flag("force"),
            ]
        ),
    )
)
def validate_handler(response: Response):
    input_flags = response.input_flags

    print("Flag validation results:")

    valid_flags: list[InputFlag] = []
    invalid_flags: list[InputFlag] = []
    undefined_flags: list[InputFlag] = []

    for flag in input_flags:
        if flag.status == ValidationStatus.VALID:
            valid_flags.append(flag)
            print(f"  ✓ {flag.string_entity}: {flag.input_value} (VALID)")
        elif flag.status == ValidationStatus.INVALID:
            invalid_flags.append(flag)
            print(f"  ✗ {flag.string_entity}: {flag.input_value} (INVALID)")
        elif flag.status == ValidationStatus.UNDEFINED:
            undefined_flags.append(flag)
            print(f"  ? {flag.string_entity}: {flag.input_value} (UNDEFINED)")

    print("\nSummary:")
    print(f"  Valid flags: {len(valid_flags)}")
    print(f"  Invalid flags: {len(invalid_flags)}")
    print(f"  Undefined flags: {len(undefined_flags)}")

    if valid_flags:
        print("\nProcessing valid flags:")
        for flag in valid_flags:
            print(f"  Processing {flag.name} = {flag.input_value}")
