import re

from argenta import Command
from argenta.command import Flag, Flags

# Создание коллекции с флагами
flags = Flags(
    [
        Flag(
            "host", possible_values=re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        ),
        Flag("port", possible_values=re.compile(r"^\d{1,5}$")),
    ]
)

# Использование в команде
cmd = Command("start", description="Start the server", flags=flags)
