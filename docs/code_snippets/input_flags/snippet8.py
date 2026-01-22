from argenta.command.flag import InputFlag, ValidationStatus
from argenta.command import InputFlags

# Create first collection
flags1 = InputFlags(
    [
        InputFlag(name="flag1", input_value="value1", status=ValidationStatus.VALID),
        InputFlag(name="flag2", input_value="value2", status=ValidationStatus.VALID),
    ]
)

# Create second collection with same flags
flags2 = InputFlags(
    [
        InputFlag(name="flag1", input_value="value1", status=ValidationStatus.VALID),
        InputFlag(name="flag2", input_value="value2", status=ValidationStatus.VALID),
    ]
)

# Create third collection with different values
flags3 = InputFlags(
    [
        InputFlag(name="flag1", input_value="different", status=ValidationStatus.VALID),
        InputFlag(name="flag2", input_value="value2", status=ValidationStatus.VALID),
    ]
)

print(f"flags1 == flags2: {flags1 == flags2}")  # True (same names)
print(
    f"flags1 == flags3: {flags1 == flags3}"
)  # True (same names, values are not considered)

# Different collections
flags4 = InputFlags(
    [InputFlag(name="flag3", input_value="value3", status=ValidationStatus.VALID)]
)
print(f"flags1 == flags4: {flags1 == flags4}")  # False (different flags)
