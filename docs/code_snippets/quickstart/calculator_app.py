import operator
import re

from argenta import App, Orchestrator, Response, Router
from argenta.app import DynamicDividingLine
from argenta.command import Command, Flag, Flags
from argenta.response.status import ResponseStatus

router = Router("Calculator")

operations = {
    'mul': operator.mul,
    'sub': operator.sub,
    'add': operator.add
}

@router.command(
    Command(
        "calc",
        description="Calculator with two numbers",
        flags=Flags(
            [
                Flag("a", possible_values=re.compile(r"^\d{,5}$")),  # First number
                Flag("b", possible_values=re.compile(r"^\d{,5}$")),  # Second number
                Flag("operation", possible_values=["add", "sub", "mul"]),  # Operation: add, sub, mul
            ]
        ),
    )
)
def calc_handler(response: Response):
    # Get flag values
    a_flag = response.input_flags.get_flag_by_name("a")
    b_flag = response.input_flags.get_flag_by_name("b")
    op_flag = response.input_flags.get_flag_by_name("op")

    # Check that all flags are provided
    if response.status != ResponseStatus.ALL_FLAGS_VALID or not all([a_flag, b_flag, op_flag]):
        print("Error: must specify --a, --b and --op")
        return

    a = float(a_flag.input_value)
    b = float(b_flag.input_value)
    operation = op_flag.input_value

    try:
        result = operations[operation](a, b)
    except ZeroDivisionError:
        print("Can't divide by zero")
    else:
        print(f"Result: {result}")


app = App(
    initial_message="Calculator",
    repeat_command_groups_printing=False,
    prompt=">> ",
    dividing_line=DynamicDividingLine("~"),
)
orchestrator = Orchestrator()


def main():
    app.include_router(router)
    orchestrator.start_polling(app)


if __name__ == "__main__":
    main()
