from argenta.command.flag import Flag, InputFlag, ValidationStatus, PossibleValues
import re

# Создаём различные типы флагов
verbose_flag = Flag("verbose", possible_values=PossibleValues.NEITHER)
output_flag = Flag("output", possible_values=PossibleValues.ALL)
level_flag = Flag("level", possible_values=["1", "2", "3"])
pattern_flag = Flag("pattern", possible_values=re.compile(r'^[a-zA-Z]+$'))

# Создаём входные флаги с различными статусами
input_flags = [
    # Валидные флаги
    InputFlag("verbose", input_value=None, status=ValidationStatus.VALID),
    InputFlag("output", input_value="result.txt", status=ValidationStatus.VALID),
    InputFlag("level", input_value="2", status=ValidationStatus.VALID),
    InputFlag("pattern", input_value="onlyletters", status=ValidationStatus.VALID),
    
    # Невалидные флаги
    InputFlag("verbose", input_value="true", status=ValidationStatus.INVALID),
    InputFlag("level", input_value="4", status=ValidationStatus.INVALID),
    InputFlag("pattern", input_value="123", status=ValidationStatus.INVALID),
    
    # Неопределённые флаги
    InputFlag("unknown", input_value="value", status=ValidationStatus.UNDEFINED),
]

# Обрабатываем все флаги
valid_count = invalid_count = undefined_count = 0

for flag in input_flags:
    if flag.status == ValidationStatus.VALID:
        valid_count += 1
    elif flag.status == ValidationStatus.INVALID:
        invalid_count += 1
    elif flag.status == ValidationStatus.UNDEFINED:
        undefined_count += 1

print(f"Валидных флагов: {valid_count}")
print(f"Невалидных флагов: {invalid_count}")
print(f"Неопределённых флагов: {undefined_count}")
