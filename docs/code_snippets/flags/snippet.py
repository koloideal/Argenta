import re
from argenta.command import Command, Flag, Flags

flags = Flags(
    [
        Flag("host", possible_values=re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")),
        Flag("port", possible_values=re.compile(r"^\d{1,5}$")),
    ]
)

cmd = Command("start", description="Start the server", flags=flags)
