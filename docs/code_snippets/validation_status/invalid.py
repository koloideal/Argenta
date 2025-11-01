from argenta.command.flag import Flag, InputFlag, PossibleValues, ValidationStatus

# Создание флага без значения
help_flag = Flag("help", possible_values=PossibleValues.NEITHER)

# Создание некорректного входного флага (передано значение, когда не должно быть)
invalid_input = InputFlag("help", input_value="please", status=ValidationStatus.INVALID)

print(f"Флаг: {invalid_input.string_entity}")
print(f"Значение: {invalid_input.input_value}")
print(f"Статус: {invalid_input.status}")  # Выведет: INVALID

# Также невалидным будет флаг с недопустимым значением из списка
mode_flag = Flag("mode", possible_values=["fast", "slow"])
invalid_mode = InputFlag("mode", input_value="medium", status=ValidationStatus.INVALID)
