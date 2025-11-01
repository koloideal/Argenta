from argenta import InputFlag, ValidationStatus

# Создание входных флагов с различными статусами
valid_flag = InputFlag(
    "output", input_value="/path/to/file.txt", status=ValidationStatus.VALID
)

invalid_flag = InputFlag(
    "count", input_value="not-a-number", status=ValidationStatus.INVALID
)

undefined_flag = InputFlag(
    "experimental", input_value="test", status=ValidationStatus.UNDEFINED
)

flags = [valid_flag, invalid_flag, undefined_flag]
for flag in flags:
    print(f"{flag.string_entity}: {flag.status.value}")
