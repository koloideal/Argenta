from argenta.command import Command
from argenta.router import Router

user_router = Router(title="User Management")


@user_router.command(Command("add-user", description="Adds a new user"))
def add_user_handler(response):
    # Логика добавления пользователя
    print("User added successfully!")
