from argenta import Router, Command, Response
from argenta.command.flag import InputFlag, ValidationStatus, InputFlags

router = Router(title="Add Flag Example")

@router.command(Command("test", description="Test command"))
def test_handler(response: Response):
    # Создаём новую коллекцию InputFlags
    new_flags = InputFlags()
    
    # Добавляем один флаг
    test_flag = InputFlag(
        name="test",
        prefix="--",
        input_value="value",
        status=ValidationStatus.VALID
    )
    new_flags.add_flag(test_flag)
    
    print(f"Flags count: {len(new_flags.flags)}")
    print(f"First flag: {new_flags.flags[0].name}")

