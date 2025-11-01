from argenta import Command, Response, Router

router = Router(title="Clear Data Example")


@router.command(Command("clear", description="Clear all stored data"))
def clear_handler(response: Response):
    # Очищаем всё хранилище данных
    response.clear_data()
    print("All data cleared")


@router.command(Command("check", description="Check if data exists"))
def check_handler(response: Response):
    data = response.get_data()
    if data:
        print(f"Storage contains {len(data)} item(s)")
    else:
        print("Storage is empty")
