from argenta import Command, Response, Router

router = Router(title="System")


@router.command(
    Command(
        "shutdown",
        description="Shutdown the system",
        aliases=["poweroff", "halt", "stop"]
    )
)
def handle_shutdown(response: Response):
    print("Shutting down the system...")