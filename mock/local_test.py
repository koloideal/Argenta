from argenta.command.flag.flags.models import InputFlags, UndefinedInputFlags
from argenta.command.flag.models import InputFlag
from argenta.command.models import Command
from argenta.router.entity import Router


router = Router()
cmd = Command('cmd')
input_flags = InputFlags([InputFlag('ssh')])
print(router._structuring_input_flags(cmd, input_flags).undefined_flags == UndefinedInputFlags([InputFlag('ssh')]))