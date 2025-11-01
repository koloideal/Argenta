from argenta.command.flag import InputFlag, ValidationStatus

flag = InputFlag(
    name="verbose", prefix="-", input_value=None, status=ValidationStatus.VALID
)

# Получение строкового представления флага
print(flag.string_entity)  # -verbose
