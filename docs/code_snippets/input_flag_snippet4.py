from argenta.command.flag import InputFlag, ValidationStatus

flag = InputFlag(
    name="config",
    prefix="--",
    input_value="settings.json",
    status=ValidationStatus.VALID
)

# Отладочное представление объекта
print(repr(flag))
# InputFlag<prefix='--', name='config', value='settings.json', status=ValidationStatus.VALID>
