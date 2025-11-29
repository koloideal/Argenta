from argenta.command.flag import InputFlag, ValidationStatus

flag = InputFlag(
    name="config",
    prefix="--",
    input_value="settings.json",
    status=ValidationStatus.VALID,
)

# Debug representation of the object
print(repr(flag))
# InputFlag<prefix='--', name='config', value='settings.json', status=ValidationStatus.VALID>
