from argenta import Router, Response, Command, DataBridge
from argenta.command import Flag
from argenta.di import FromDishka

router = Router(title="Authentication")

def authenticate_user(username: str) -> str:
    return f"token_for_{username}"


@router.command(Command("login", flags=Flag("username")))
def login_handler(response: Response, data_bridge: FromDishka[DataBridge]):
    username_flag = response.input_flags.get_flag_by_name("username")
    if not username_flag or not username_flag.input_value:
        print("Ошибка необходимо указать имя пользователя с помощью флага --username.")
        return

    username = username_flag.input_value
    token = authenticate_user(username)

    data_bridge.update({"auth_token": token})
    print(f"Успешный вход! Пользователь '{username}' аутентифицирован.")


@router.command("get-profile")
def get_profile_handler(response: Response, data_bridge: FromDishka[DataBridge])
    token = data_bridge.get_by_key("auth_token")

    if not token:
        print("Ошибка: вы не аутентифицированы. Сначала выполните команду 'login'.")
        return

    print(f"Загрузка профиля с использованием токена: [yellow]{token}[/yellow]")


@router.command("logout")
def logout_handler(response: Response, data_bridge: FromDishka[DataBridge]):
    try:
        data_bridge.delete_by_key("auth_token")
        print("Выход выполнен. Данные сессии очищены.")
    except KeyError:
        print("Вы и так не были аутентифицированы.")
