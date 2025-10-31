from argenta import InputFlag, ValidationStatus

flag1 = InputFlag(
    name="debug",
    prefix="--",
    input_value=None,
    status=ValidationStatus.VALID
)

flag2 = InputFlag(
    name="debug",
    prefix="-",
    input_value="true",
    status=ValidationStatus.INVALID
)

# Сравнение по имени (префикс и значение не учитываются)
if flag1 == flag2:
    print("Флаги имеют одинаковое имя")  # Выведется
