from argenta import Command, Response, Router

router = Router(title="Data Example")


@router.command(Command("set", description="Set data"))
def set_handler(response: Response):
    # Обновляем глобальное хранилище данных
    response.update_data(
        {
            "user_name": "John",
            "timestamp": "2024-01-01",
            "settings": {"theme": "dark", "language": "ru"},
        }
    )
    print("Data updated successfully")


@router.command(Command("show", description="Show data"))
def show_handler(response: Response):
    # Получаем данные из глобального хранилища
    data = response.get_data()
    if "user_name" in data:
        print(f"User: {data['user_name']}")
        print(f"Settings: {data.get('settings', {})}")
