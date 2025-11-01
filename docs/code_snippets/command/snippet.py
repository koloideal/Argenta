from argenta import Command
from argenta.command import Flag, Flags

# Простая команда без флагов
hello_cmd = Command("hello", description="Greet the user")

# Команда с описанием и псевдонимами
quit_cmd = Command("quit", description="Exit the application", aliases=["exit", "q"])

# Команда с флагами
deploy_cmd = Command(
    "deploy",
    description="Deploy application to server",
    flags=Flags(
        [
            Flag("env", help="Environment name", possible_values=["dev", "prod"]),
            Flag("force", help="Force deployment"),
        ]
    ),
    aliases=["dep"],
)
