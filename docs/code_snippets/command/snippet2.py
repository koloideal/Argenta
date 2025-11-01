from argenta import Command, Response, Router

router = Router(title="User Management")


@router.command(Command("create-user", description="Create a new user account"))
def handle_create_user(response):
    print("Creating new user...")


@router.command(
    Command(
        "delete-user",
        description="Delete existing user account",
        aliases=["remove-user", "rm-user"],
    )
)
def handle_delete_user(response: Response):
    print("Deleting user...")
