from argenta import Command, Response, Router

user_router = Router(title="User Management")

@user_router.command(Command("add-user", description="Adds a new user"))
def add_user_handler(response: Response):
    print("User added successfully!")
