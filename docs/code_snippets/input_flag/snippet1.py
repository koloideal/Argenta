from argenta.command.flag import InputFlag, ValidationStatus

# Создание InputFlag с полным набором параметров
output_flag = InputFlag(
    name="output", prefix="--", input_value="result.txt", status=ValidationStatus.VALID
)

# Флаг без значения
help_flag = InputFlag(
    name="help", prefix="-", input_value=None, status=ValidationStatus.VALID
)
