from argenta import Command, Response, Router
from argenta.response import ResponseStatus

router = Router(title="Example")

@router.command(Command("greet", description="Greet the user"))
def greet_handler(response: Response):
    # response автоматически передаётся в обработчик
    # response.status содержит статус валидации флагов
    # response.input_flags содержит все введённые флаги
    
    if response.status == ResponseStatus.ALL_FLAGS_VALID:
        print("Hello! All flags are valid.")
    else:
        print("Warning: Some flags have issues.")

