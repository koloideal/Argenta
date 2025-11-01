from argenta.command.flag import InputFlag, ValidationStatus
from argenta.command.flag.flags.models import InputFlags

# Создаём первую коллекцию
flags1 = InputFlags(
    [
        InputFlag(name="flag1", input_value="value1", status=ValidationStatus.VALID),
        InputFlag(name="flag2", input_value="value2", status=ValidationStatus.VALID),
    ]
)

# Создаём вторую коллекцию с теми же флагами
flags2 = InputFlags(
    [
        InputFlag(name="flag1", input_value="value1", status=ValidationStatus.VALID),
        InputFlag(name="flag2", input_value="value2", status=ValidationStatus.VALID),
    ]
)

# Создаём третью коллекцию с другими флагами
flags3 = InputFlags(
    [
        InputFlag(name="flag1", input_value="different", status=ValidationStatus.VALID),
        InputFlag(name="flag2", input_value="value2", status=ValidationStatus.VALID),
    ]
)

print(f"flags1 == flags2: {flags1 == flags2}")  # True (одинаковые имена)
print(
    f"flags1 == flags3: {flags1 == flags3}"
)  # True (имена одинаковые, значения не учитываются)

# Разные коллекции
flags4 = InputFlags(
    [InputFlag(name="flag3", input_value="value3", status=ValidationStatus.VALID)]
)
print(f"flags1 == flags4: {flags1 == flags4}")  # False (разные флаги)
