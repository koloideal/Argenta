from argenta import Command, Response, Router

router = Router(title="Delete Data Example")


@router.command(Command("store", description="Store data"))
def store_handler(response: Response):
    response.update_data(
        {
            "temp_key": "temporary value",
            "important_key": "important value",
            "another_key": "another value",
        }
    )
    print("Data stored")


@router.command(Command("remove", description="Remove specific key"))
def remove_handler(response: Response):
    # Delete specific key from storage
    try:
        response.delete_from_data("temp_key")
        print("Key 'temp_key' deleted")

        # Check what remains
        remaining = response.get_data()
        print(f"Remaining keys: {list(remaining.keys())}")
    except KeyError:
        print("Key not found")
