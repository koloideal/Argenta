from argenta import Command, Response, Router
from argenta.command.flag import InputFlag, ValidationStatus
from argenta.command import InputFlags

router = Router(title="Add Flag Example")


@router.command(Command("test", description="Test command"))
def test_handler(response: Response):
    # Create new InputFlags collection
    new_flags = InputFlags()

    # Add one flag
    test_flag = InputFlag(
        name="test", prefix="--", input_value="value", status=ValidationStatus.VALID
    )
    new_flags.add_flag(test_flag)

    print(f"Flags count: {len(new_flags.flags)}")
    print(f"First flag: {new_flags.flags[0].name}")
