from argenta.command.flag import InputFlag, ValidationStatus
from argenta.command import InputFlags

# Create InputFlags collection
flags = InputFlags()

# Create several flags
flag1 = InputFlag(name="option1", prefix="--", input_value="value1", status=ValidationStatus.VALID)

flag2 = InputFlag(name="option2", prefix="--", input_value="value2", status=ValidationStatus.VALID)

flag3 = InputFlag(name="option3", prefix="---", input_value="value3", status=ValidationStatus.VALID)

# Add all flags in one call
flags.add_flags([flag1, flag2, flag3])

print(f"Total flags: {len(flags.flags)}")
for flag in flags:
    print(f"  - {flag.string_entity}: {flag.input_value}")
