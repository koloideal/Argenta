from argenta import Command, Response, Router
from argenta.command import Flag, Flags
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

    # Итерируемся по всем флагам и проверяем их статусы
    print("Flag validation results:")

    valid_flags = []
    invalid_flags = []
    undefined_flags = []

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

    # Выводим сводку
    print("\nSummary:")
    print(f"  Valid flags: {len(valid_flags)}")
    print(f"  Invalid flags: {len(invalid_flags)}")
    print(f"  Undefined flags: {len(undefined_flags)}")

    # Обрабатываем только валидные флаги
    if valid_flags:
        print("\nProcessing valid flags:")
        for flag in valid_flags:
            print(f"  Processing {flag.name} = {flag.input_value}")
