from argenta import InputFlag, ValidationStatus

flag_with_value = InputFlag(
    name="output",
    prefix="--",
    input_value="result.txt",
    status=ValidationStatus.VALID
)

flag_without_value = InputFlag(
    name="help",
    prefix="-",
    input_value=None,
    status=ValidationStatus.VALID
)

# Строковое представление включает значение
print(str(flag_with_value))  # --output result.txt
print(str(flag_without_value))  # -help None
