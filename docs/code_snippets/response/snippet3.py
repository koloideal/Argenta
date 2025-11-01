from argenta import Command, Response, Router

router = Router(title="Get Data Example")


@router.command(Command("info", description="Show all stored data"))
def info_handler(response: Response):
    # Получаем все данные из глобального хранилища
    all_data = response.get_data()

    if all_data:
        print("Stored data:")
        for key, value in all_data.items():
            print(f"  {key}: {value}")
    else:
        print("No data stored")
