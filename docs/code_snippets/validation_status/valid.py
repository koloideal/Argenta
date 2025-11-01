from argenta.command.flag import Flag, InputFlag, ValidationStatus

# Создание флага, который принимает только определённые значения
log_level_flag = Flag(
    "log-level", possible_values=["debug", "info", "warning", "error"]
)

# Создание корректного входного флага
valid_input = InputFlag("log-level", input_value="debug", status=ValidationStatus.VALID)

print(f"Флаг: {valid_input.string_entity}")
print(f"Значение: {valid_input.input_value}")
print(f"Статус: {valid_input.status}")  # Выведет: VALID
