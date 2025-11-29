from argenta.command import Flag, Flags, Command

# Simple command without flags
hello_cmd = Command("hello", description="Greet the user")

# Command with description and aliases
quit_cmd = Command("quit", description="Exit the application", aliases=["exit", "q"])

# Command with flags
deploy_cmd = Command(
    "deploy",
    description="Deploy application to server",
    flags=Flags(
        [
            Flag("env", possible_values=["dev", "prod"]),
            Flag("force"),
        ]
    ),
    aliases=["dep"],
)
