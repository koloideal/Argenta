from argenta import Router, Response, Command, DataBridge
from argenta.command import Flag
from argenta.di import FromDishka

# 1. Создаём роутер
router = Router(title='Authentication')

# 2. Определяем сервис и обработчики
def authenticate_user(username: str) -> str:
    """Возвращает фиктивный токен для пользователя."""
    return f"token_for_{username}"

@router.command(Command('login', flags=Flag('username')))
def login_handler(response: Response, data_bridge: FromDishka[DataBridge]):
    """Обработчик для команды 'login'. Сохраняет токен в хранилище."""
    username_flag = response.input_flags.get_flag_by_name('username')
    if not username_flag or not username_flag.input_value:
        print("[red]Ошибка:[/red] необходимо указать имя пользователя с помощью флага --username.")
        return

    username = username_flag.input_value
    token = authenticate_user(username)

    # Сохраняем токен в общем хранилище сессии
    data_bridge.update({"auth_token": token})
    print(f"[green]Успешный вход![/green] Пользователь '{username}' аутентифицирован.")

@router.command('get-profile')
def get_profile_handler(response: Response, data_bridge: FromDishka[DataBridge]):
    """Обработчик для команды 'get-profile'. Использует токен из хранилища."""
    session_data = data_bridge.get_all()
    token = session_data.get("auth_token")

    if not token:
        print("[red]Ошибка:[/red] вы не аутентифицированы. Сначала выполните команду 'login'.")
        return

    print(f"Загрузка профиля с использованием токена: [yellow]{token}[/yellow]")

@router.command('logout')
def logout_handler(response: Response, data_bridge: FromDishka[DataBridge]):
    """Обработчик для команды 'logout'. Очищает токен."""
    try:
        data_bridge.delete_by_key("auth_token")
        print("[green]Выход выполнен.[/green] Данные сессии очищены.")
    except KeyError:
        print("Вы и так не были аутентифицированы.")

