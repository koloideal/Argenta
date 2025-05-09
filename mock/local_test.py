from argenta.app import App
from argenta.app.autocompleter import AutoCompleter
from argenta.router import Router
from argenta.command import Command
from argenta.orchestrator import Orchestrator
from argenta.app.dividing_line import DynamicDividingLine
from argenta.response import Response
import platform
import psutil
import os
import subprocess
import socket

# Маршрутизатор для работы с файлами
file_router = Router("Файловые операции")

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

# Маршрутизатор для системных операций
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

# Маршрутизатор для сетевых операций
network_router = Router("Сетевые операции")

@network_router.command(Command("ping", "Проверка доступности хоста"))
def ping_host(response: Response):
    host = input("Введите имя хоста: ")
    print(f"Пингую {host}...")
    subprocess.run(["ping", "-c", "4", host])

@network_router.command(Command("ip", "Показать IP-адреса"))
def show_ip(response: Response):
    hostname = socket.gethostname()
    print(f"Имя хоста: {hostname}")
    print(f"IP-адрес: {socket.gethostbyname(hostname)}")

# Создание приложения и регистрация маршрутизаторов
app = App(
    prompt="System> ",
    initial_message="Системный монитор v1.0",
    dividing_line=DynamicDividingLine("*"),
    autocompleter=AutoCompleter('.hist')
)

# Добавляем все маршрутизаторы
app.include_routers(file_router, system_router, network_router)

# Добавляем сообщение при запуске
app.add_message_on_startup("Для просмотра доступных команд нажмите Enter")

# Запускаем приложение
orchestrator = Orchestrator()
orchestrator.start_polling(app)