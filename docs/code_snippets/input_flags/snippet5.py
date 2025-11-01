from argenta import Command, Response, Router
from argenta.command import Flag, Flags

router = Router(title="Iterate Example")

@router.command(Command(
    "process",
    description="Process with multiple flags",
    flags=Flags([
        Flag("file"),
        Flag("format"),
        Flag("output")
    ])
))
def process_handler(response: Response):
    input_flags = response.input_flags
    
    # Итерируемся по всем введённым флагам
    print("All flags:")
    for flag in input_flags:
        status_str = flag.status.name if flag.status else "None"
        print(f"  {flag.string_entity}: {flag.input_value} (status: {status_str})")
    
    # Также можно использовать enumerate для получения индексов
    print("\nFlags with indices:")
    for index, flag in enumerate(input_flags):
        print(f"  [{index}] {flag.name}: {flag.input_value}")

