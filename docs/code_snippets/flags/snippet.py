from argenta.command import Flags, Flag
from argenta import Command
import re


# Создание коллекции с флагами
flags = Flags([
    Flag("host", possible_values=re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")),
    Flag("port", possible_values=re.compile(r"^\d{1,5}$"))
])

# Использование в команде
cmd = Command(
    "start",
    description="Start the server",
    flags=flags
)