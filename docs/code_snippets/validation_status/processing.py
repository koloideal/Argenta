from argenta import InputFlag, ValidationStatus


def process_input_flag(input_flag: InputFlag) -> None:
    """Обрабатывает входной флаг в зависимости от его статуса валидации"""

    if input_flag.status == ValidationStatus.VALID:
        print(f"✓ Обрабатываем валидный флаг: {input_flag.string_entity}")
        # Выполняем основную логику
        execute_flag_logic(input_flag)

    elif input_flag.status == ValidationStatus.INVALID:
        print(f"✗ Ошибка валидации флага: {input_flag.string_entity}")
        # Записываем ошибку и прекращаем выполнение
        log_validation_error(input_flag)

    elif input_flag.status == ValidationStatus.UNDEFINED:
        print(f"? Неопределённый статус флага: {input_flag.string_entity}")
        # Пытаемся провести валидацию или пропускаем
        attempt_revalidation(input_flag)


def execute_flag_logic(flag: InputFlag) -> None:
    """Выполняет логику для валидного флага"""
    pass


def log_validation_error(flag: InputFlag) -> None:
    """Записывает ошибку валидации в лог"""
    pass


def attempt_revalidation(flag: InputFlag) -> None:
    """Пытается повторно провести валидацию"""
    pass
