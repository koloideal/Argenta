from rich.console import Console

from argenta.app import App
from argenta.app.autocompleter import AutoCompleter
from argenta.router import Router
from argenta.command import Command
from argenta.response import Response
from argenta.orchestrator import Orchestrator
from argenta.app.dividing_line import DynamicDividingLine, StaticDividingLine
import platform
import psutil
import os
import subprocess
import socket

# Создаем маршрутизатор для работы с файлами
file_router = Router("Файловые операции", disable_redirect_stdout=True)

@file_router.command(Command("list", "Список файлов"))
def list_files(response: Response):
    files = os.listdir()
    for file in files:
        print(file)

@file_router.command(Command("size", "Размер файла"))
def file_size(response: Response):
    file_name = input("Введите имя файла: ")
    if os.path.exists(file_name):
        size = os.path.getsize(file_name)
        print(f"Размер файла {file_name}: {size} байт")
    else:
        print(f"Файл {file_name} не найден")

# Создаем маршрутизатор для системных операций
system_router = Router("Системные операции")

@system_router.command(Command("info", "Информация о системе"))
def system_info(response: Response):
    print(f"Система: {platform.system()}")
    print(f"Версия: {platform.version()}")
    print(f"Архитектура: {platform.architecture()}")
    print(f"Процессор: {platform.processor()}")

@system_router.command(Command("memory", "Информация о памяти"))
def memory_info(response: Response):
    memory = psutil.virtual_memory()
    print(f"Всего памяти: {memory.total / (1024**3):.2f} ГБ")
    print(f"Доступно: {memory.available / (1024**3):.2f} ГБ")
    print(f"Использовано: {memory.used / (1024**3):.2f} ГБ ({memory.percent}%)")

# Создаем маршрутизатор для сетевых операций
network_router = Router("Сетевые операции", disable_redirect_stdout=True)

@network_router.command(Command("ping", "Проверка доступности хоста"))
def ping_host(response: Response):
    host = input("Введите имя хоста: ")
    print(f"Пингую {host}...")
    subprocess.run(["ping", host])

@network_router.command(Command("ip", "Показать IP-адреса"))
def show_ip(response: Response):
    hostname = socket.gethostname()
    print(f"Имя хоста: {hostname}")
    print(f"IP-адрес: {socket.gethostbyname(hostname)}")

# Создаем маршрутизатор для работы с пользователями
user_router = Router("Операции с пользователями")

@user_router.command(Command("create", "Создать пользователя"))
def create_user(response: Response):
    username = input("Введите имя пользователя: ")
    print(f"Пользователь {username} создан")

@user_router.command(Command("delete", "Удалить пользователя"))
def delete_user(response: Response):
    username = input("Введите имя пользователя: ")
    print(f"Пользователь {username} удален")

# Создаем приложение и регистрируем маршрутизаторы
app = App(
    prompt="MyApp> ",
    initial_message="Caser",
    farewell_message="Pokeda",
    dividing_line=DynamicDividingLine("*"),
    repeat_command_groups=False,
    ignore_command_register=True,
    override_system_messages=False,
    autocompleter=AutoCompleter('.history')
)

app.include_routers(file_router, system_router, network_router, user_router)

# Добавляем сообщение при запуске
app.add_message_on_startup("\nДля просмотра доступных команд нажмите Enter")

# Пользовательский обработчик пустых команд
def empty_command_handler():
    print("Для выхода введите Q")

app.set_empty_command_handler(empty_command_handler)

# Запускаем приложение
orchestrator = Orchestrator()
orchestrator.start_polling(app)
