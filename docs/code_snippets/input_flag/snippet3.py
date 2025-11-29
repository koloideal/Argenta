from argenta.command.flag import InputFlag, ValidationStatus

flag_with_value = InputFlag(
    name="output", prefix="--", input_value="result.txt", status=ValidationStatus.VALID
)

flag_without_value = InputFlag(
    name="help", prefix="-", input_value=None, status=ValidationStatus.VALID
)

# String representation includes value
print(str(flag_with_value))  # --output result.txt
print(str(flag_without_value))  # -help None
