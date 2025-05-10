from argenta.router import Router
from argenta.command import Command
from argenta.response import Response
from argenta.response.status import Status
from argenta.command.flag import Flag
from argenta.command.flags import Flags
from argenta.app import App
from argenta.orchestrator import Orchestrator

# Создание маршрутизатора
file_router = Router("Операции с файлами")

# Определение флагов для команды копирования
copy_flags = Flags(
    Flag('source', '--'),
    Flag('destination', '--'),
    Flag('recursive', '--', False),  # Булевый флаг без значения
    Flag('force', '-', False)        # Короткий булевый флаг
)

# Регистрация команды копирования
@file_router.command(Command(
    trigger="copy",
    description="Копирование файлов",
    flags=copy_flags,
    aliases=["cp"]
))
def copy_files(response: Response):
    # Получаем значения корректных флагов
    source = None
    destination = None
    recursive = False
    force = False

    for flag in response.valid_flags:
        if flag.get_name() == "source":
            source = flag.get_value()
        elif flag.get_name() == "destination":
            destination = flag.get_value()
        elif flag.get_name() == "recursive":
            recursive = True
        elif flag.get_name() == "force":
            force = True

    # Проверка обязательных параметров
    if not source or not destination:
        print("Ошибка: необходимо указать источник и назначение")
        return

    print(f"Копирование из {source} в {destination}")
    if recursive:
        print("Рекурсивное копирование включено")
    if force:
        print("Принудительное копирование включено")

    # Обработка неопределенных флагов
    if response.undefined_flags:
        print("\nПредупреждение: обнаружены незарегистрированные флаги:")
        for flag in response.undefined_flags:
            print(f"  - {flag.get_name()}" +
                 (f" = {flag.get_value()}" if flag.get_value() else ""))

    # Обработка флагов с некорректными значениями
    if response.invalid_value_flags:
        print("\nПредупреждение: обнаружены флаги с некорректными значениями:")
        for flag in response.invalid_value_flags:
            print(f"  - {flag.get_name()} = {flag.get_value()}")

    # Принятие решения на основе статуса
    if response.status != Status.ALL_FLAGS_VALID:
        print("\nВыполнение с предупреждениями из-за проблем с флагами.")



app = App()
app.include_router(file_router)
orchestrator = Orchestrator()

orchestrator.start_polling(app)







