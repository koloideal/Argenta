from argenta import InputFlag, ValidationStatus

# Создание входного флага без определения статуса
undefined_input = InputFlag("unknown-flag", input_value="some-value", status=ValidationStatus.UNDEFINED)

print(f"Флаг: {undefined_input.string_entity}")
print(f"Значение: {undefined_input.input_value}")
print(f"Статус: {undefined_input.status.value}")  # Выведет: UNDEFINED

# Или флаг, для которого валидация ещё не проводилась
pending_input = InputFlag("pending", input_value=None, status=ValidationStatus.UNDEFINED)
