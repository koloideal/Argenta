from argenta import Router, Response
from argenta.command import Command, Flag, PossibleValues
from argenta.command.flag import ValidationStatus

router = Router()


@router.command(Command("deploy", flags=Flag("verbose", possible_values=PossibleValues.NEITHER)))
def deploy_handler(response: Response):
    # Check for toggle flag presence
    verbose_flag = response.input_flags.get_flag_by_name("verbose")

    if verbose_flag and verbose_flag.status == ValidationStatus.VALID:
        print("Deploying with verbose output...")
        # Detailed logic
    elif verbose_flag and verbose_flag.status == ValidationStatus.INVALID:
        print("Incorrect flag value")
        return
    else:
        print("Deploying...")
        # Normal logic
