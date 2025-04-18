# Argenta

Python library for creating TUI

![preview](https://github.com/koloideal/Argenta/blob/kolo/imgs/mock_app_preview_last.png?raw=True)  
Пример внешнего вида TUI, написанного с помощью Argenta  

---

# Installing
```bash
pip install argenta
```
or
```bash
poetry add argenta
```

---

# Quick start

Example of the simplest TUI with a single command 
```python
# routers.py
from argenta.router import Router
from argenta.command import Command


router = Router()

@router.command(Command("hello"))
def handler():
  print("Hello, world!")
```

```python
# main.py
from argenta.app import App
from argenta.orchestrator import Orchestrator
from routers import router

app: App = App()
orchestrator: Orchestrator = Orchestrator()


def main() -> None:
    app.include_router(router)
    orchestrator.start_polling(app)


if __name__ == '__main__':
    main()
```
Пример оболочки с командой, у которой зарегистрированы флаги

```python
# routers.py
import re
from argenta.router import Router
from argenta.command import Command
from argenta.orchestrator import Orchestrator
from argenta.command.flag.defaults import PredefinedFlags
from argenta.command.flag import Flags, Flag, InputFlags

router = Router()

registered_flags = Flags(PredefinedFlags.HOST,
                         Flag('port', '--', re.compile(r'^[0-9]{1,4}$')))


@router.command(Command("hello"))
def handler():
    print("Hello, world!")


@router.command(Command(trigger="ssh",
                        description='connect via ssh',
                        flags=registered_flags))
def handler_with_flags(flags: InputFlags):
    for flag in flags:
        print(f'Flag name: {flag.get_name()}\n'
              f'Flag value: {flag.get_value()}')
```

---

<a id="argenta.app.autocompleter.entity"></a>

# `argenta.app.autocompleter`

<a id="argenta.app.autocompleter.entity.AutoCompleter"></a>

## AutoCompleter Objects

```python
class AutoCompleter()
```
---
<a id="argenta.app.autocompleter.entity.AutoCompleter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(history_filename: str = False,
             autocomplete_button: str = 'tab') -> None
```

Public. Configures and implements auto-completion of input command

**Arguments**:

- `history_filename`: the name of the file for saving the history of the autocompleter
- `autocomplete_button`: the button for auto-completion

**Returns**:

None

<a id="argenta.app.autocompleter.entity.AutoCompleter.complete"></a>

#### complete

```python
def complete(text, state) -> str | None
```

Private. Auto-completion function

**Arguments**:

- `text`: part of the command being entered
- `state`: the current cursor position is relative to the beginning of the line

**Returns**:

the desired candidate as str or None

<a id="argenta.app.autocompleter.entity.AutoCompleter.initial_setup"></a>

#### initial\_setup

```python
def initial_setup(all_commands: list[str]) -> None
```

Public. Initial setup function

**Arguments**:

- `all_commands`: Registered commands for adding them to the autocomplete history

**Returns**:

None

<a id="argenta.app.autocompleter.entity.AutoCompleter.exit_setup"></a>

#### exit\_setup

```python
def exit_setup() -> None
```

Public. Exit setup function

**Returns**:

None

<a id="argenta.app.autocompleter.entity.AutoCompleter.get_history_items"></a>

#### get\_history\_items

```python
@staticmethod
def get_history_items() -> list[str] | list
```

Private. Returns a list of all commands entered by the user

**Returns**:

all commands entered by the user as list[str]

<a id="argenta.app.defaults"></a>

# argenta.app.defaults

<a id="argenta.app.defaults.PredefinedMessages"></a>

## PredefinedMessages Objects

```python
@dataclass
class PredefinedMessages()
```

Public. A dataclass with predetermined messages for quick use

<a id="argenta.app.dividing_line.models"></a>

# argenta.app.dividing\_line.models

<a id="argenta.app.dividing_line.models.BaseDividingLine"></a>

## BaseDividingLine Objects

```python
class BaseDividingLine(ABC)
```

<a id="argenta.app.dividing_line.models.BaseDividingLine.__init__"></a>

#### \_\_init\_\_

```python
def __init__(unit_part: str = '-') -> None
```

Private. The basic dividing line

**Arguments**:

- `unit_part`: the single part of the dividing line

**Returns**:

None

<a id="argenta.app.dividing_line.models.BaseDividingLine.get_unit_part"></a>

#### get\_unit\_part

```python
def get_unit_part() -> str
```

Private. Returns the unit part of the dividing line

**Returns**:

unit_part of dividing line as str

<a id="argenta.app.dividing_line.models.StaticDividingLine"></a>

## StaticDividingLine Objects

```python
class StaticDividingLine(BaseDividingLine)
```

<a id="argenta.app.dividing_line.models.StaticDividingLine.__init__"></a>

#### \_\_init\_\_

```python
def __init__(unit_part: str = '-', length: int = 25) -> None
```

Public. The static dividing line

**Arguments**:

- `unit_part`: the single part of the dividing line
- `length`: the length of the dividing line

**Returns**:

None

<a id="argenta.app.dividing_line.models.StaticDividingLine.get_full_static_line"></a>

#### get\_full\_static\_line

```python
def get_full_static_line(is_override: bool) -> str
```

Private. Returns the full line of the dividing line

**Arguments**:

- `is_override`: has the default text layout been redefined

**Returns**:

full line of dividing line as str

<a id="argenta.app.dividing_line.models.DynamicDividingLine"></a>

## DynamicDividingLine Objects

```python
class DynamicDividingLine(BaseDividingLine)
```

<a id="argenta.app.dividing_line.models.DynamicDividingLine.__init__"></a>

#### \_\_init\_\_

```python
def __init__(unit_part: str = '-') -> None
```

Public. The dynamic dividing line

**Arguments**:

- `unit_part`: the single part of the dividing line

**Returns**:

None

<a id="argenta.app.dividing_line.models.DynamicDividingLine.get_full_dynamic_line"></a>

#### get\_full\_dynamic\_line

```python
def get_full_dynamic_line(length: int, is_override: bool) -> str
```

Private. Returns the full line of the dividing line

**Arguments**:

- `length`: the length of the dividing line
- `is_override`: has the default text layout been redefined

**Returns**:

full line of dividing line as str

<a id="argenta.app.dividing_line"></a>

# argenta.app.dividing\_line

<a id="argenta.app.exceptions"></a>

# argenta.app.exceptions

<a id="argenta.app.exceptions.NoRegisteredHandlersException"></a>

## NoRegisteredHandlersException Objects

```python
class NoRegisteredHandlersException(Exception)
```

The router has no registered handlers

<a id="argenta.app.models"></a>

# argenta.app.models

<a id="argenta.app.models.BaseApp"></a>

## BaseApp Objects

```python
class BaseApp()
```

<a id="argenta.app.models.BaseApp.set_description_message_pattern"></a>

#### set\_description\_message\_pattern

```python
def set_description_message_pattern(
        pattern: Callable[[str, str], str]) -> None
```

Public. Sets the output pattern of the available commands

**Arguments**:

- `pattern`: output pattern of the available commands

**Returns**:

None

<a id="argenta.app.models.BaseApp.set_invalid_input_flags_handler"></a>

#### set\_invalid\_input\_flags\_handler

```python
def set_invalid_input_flags_handler(handler: Callable[[str], None]) -> None
```

Public. Sets the handler for incorrect flags when entering a command

**Arguments**:

- `handler`: handler for incorrect flags when entering a command

**Returns**:

None

<a id="argenta.app.models.BaseApp.set_repeated_input_flags_handler"></a>

#### set\_repeated\_input\_flags\_handler

```python
def set_repeated_input_flags_handler(handler: Callable[[str], None]) -> None
```

Public. Sets the handler for repeated flags when entering a command

**Arguments**:

- `handler`: handler for repeated flags when entering a command

**Returns**:

None

<a id="argenta.app.models.BaseApp.set_unknown_command_handler"></a>

#### set\_unknown\_command\_handler

```python
def set_unknown_command_handler(handler: Callable[[str], None]) -> None
```

Public. Sets the handler for unknown commands when entering a command

**Arguments**:

- `handler`: handler for unknown commands when entering a command

**Returns**:

None

<a id="argenta.app.models.BaseApp.set_empty_command_handler"></a>

#### set\_empty\_command\_handler

```python
def set_empty_command_handler(handler: Callable[[], None]) -> None
```

Public. Sets the handler for empty commands when entering a command

**Arguments**:

- `handler`: handler for empty commands when entering a command

**Returns**:

None

<a id="argenta.app.models.BaseApp.set_exit_command_handler"></a>

#### set\_exit\_command\_handler

```python
def set_exit_command_handler(handler: Callable[[], None]) -> None
```

Public. Sets the handler for exit command when entering a command

**Arguments**:

- `handler`: handler for exit command when entering a command

**Returns**:

None

<a id="argenta.app.models.App"></a>

## App Objects

```python
class App(BaseApp)
```

<a id="argenta.app.models.App.__init__"></a>

#### \_\_init\_\_

```python
def __init__(prompt: str = '[italic dim bold]What do you want to do?\n',
             initial_message: str = '\nArgenta\n',
             farewell_message: str = '\nSee you\n',
             exit_command: Command = Command('Q', 'Exit command'),
             system_router_title: str | None = 'System points:',
             ignore_command_register: bool = True,
             dividing_line: StaticDividingLine
             | DynamicDividingLine = StaticDividingLine(),
             repeat_command_groups: bool = True,
             override_system_messages: bool = False,
             autocompleter: AutoCompleter = AutoCompleter(),
             print_func: Callable[[str], None] = Console().print) -> None
```

Public. The essence of the application itself.

Configures and manages all aspects of the behavior and presentation of the user interacting with the user

**Arguments**:

- `prompt`: displayed before entering the command
- `initial_message`: displayed at the start of the app
- `farewell_message`: displayed at the end of the app
- `exit_command`: the entity of the command that will be terminated when entered
- `system_router_title`: system router title
- `ignore_command_register`: whether to ignore the case of the entered commands
- `dividing_line`: the entity of the dividing line
- `repeat_command_groups`: whether to repeat the available commands and their description
- `override_system_messages`: whether to redefine the default formatting of system messages
- `autocompleter`: the entity of the autocompleter
- `print_func`: system messages text output function

**Returns**:

None

<a id="argenta.app.models.App.run_polling"></a>

#### run\_polling

```python
def run_polling() -> None
```

Private. Starts the user input processing cycle

**Returns**:

None

<a id="argenta.app.models.App.include_router"></a>

#### include\_router

```python
def include_router(router: Router) -> None
```

Public. Registers the router in the application

**Arguments**:

- `router`: registered router

**Returns**:

None

<a id="argenta.app.models.App.include_routers"></a>

#### include\_routers

```python
def include_routers(*routers: Router) -> None
```

Public. Registers the routers in the application

**Arguments**:

- `routers`: registered routers

**Returns**:

None

<a id="argenta.app.models.App.add_message_on_startup"></a>

#### add\_message\_on\_startup

```python
def add_message_on_startup(message: str) -> None
```

Public. Adds a message that will be displayed when the application is launched

**Arguments**:

- `message`: the message being added

**Returns**:

None

<a id="argenta.app.registered_routers.entity"></a>

# argenta.app.registered\_routers.entity

<a id="argenta.app.registered_routers.entity.RegisteredRouters"></a>

## RegisteredRouters Objects

```python
class RegisteredRouters()
```

<a id="argenta.app.registered_routers.entity.RegisteredRouters.__init__"></a>

#### \_\_init\_\_

```python
def __init__(registered_routers: list[Router] = None) -> None
```

Private. Combines registered routers

**Arguments**:

- `registered_routers`: list of the registered routers

**Returns**:

None

<a id="argenta.app.registered_routers.entity.RegisteredRouters.get_registered_routers"></a>

#### get\_registered\_routers

```python
def get_registered_routers() -> list[Router]
```

Private. Returns the registered routers

**Returns**:

registered routers as list[Router]

<a id="argenta.app.registered_routers.entity.RegisteredRouters.add_registered_router"></a>

#### add\_registered\_router

```python
def add_registered_router(router: Router) -> None
```

Private. Adds a new registered router

**Arguments**:

- `router`: registered router

**Returns**:

None

<a id="argenta.app.registered_routers.entity.RegisteredRouters.add_registered_routers"></a>

#### add\_registered\_routers

```python
def add_registered_routers(*routers: Router) -> None
```

Private. Adds new registered routers

**Arguments**:

- `routers`: registered routers

**Returns**:

None

<a id="argenta.app.registered_routers"></a>

# argenta.app.registered\_routers

<a id="argenta.app"></a>

# argenta.app

<a id="argenta.command.exceptions"></a>

# argenta.command.exceptions

<a id="argenta.command.exceptions.BaseInputCommandException"></a>

## BaseInputCommandException Objects

```python
class BaseInputCommandException(Exception)
```

Private. Base exception class for all exceptions raised when parse input command

<a id="argenta.command.exceptions.UnprocessedInputFlagException"></a>

## UnprocessedInputFlagException Objects

```python
class UnprocessedInputFlagException(BaseInputCommandException)
```

Private. Raised when an unprocessed input flag is detected

<a id="argenta.command.exceptions.RepeatedInputFlagsException"></a>

## RepeatedInputFlagsException Objects

```python
class RepeatedInputFlagsException(BaseInputCommandException)
```

Private. Raised when repeated input flags are detected

<a id="argenta.command.exceptions.EmptyInputCommandException"></a>

## EmptyInputCommandException Objects

```python
class EmptyInputCommandException(BaseInputCommandException)
```

Private. Raised when an empty input command is detected

<a id="argenta.command.flag.defaults"></a>

# argenta.command.flag.defaults

<a id="argenta.command.flag.defaults.PredefinedFlags"></a>

## PredefinedFlags Objects

```python
@dataclass
class PredefinedFlags()
```

Public. A dataclass with predefined flags and most frequently used flags for quick use

<a id="argenta.command.flag.models"></a>

# argenta.command.flag.models

<a id="argenta.command.flag.models.BaseFlag"></a>

## BaseFlag Objects

```python
class BaseFlag(ABC)
```

<a id="argenta.command.flag.models.BaseFlag.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str, prefix: Literal['-', '--', '---'] = '--') -> None
```

Private. Base class for flags

**Arguments**:

- `name`: the name of the flag
- `prefix`: the prefix of the flag

**Returns**:

None

<a id="argenta.command.flag.models.BaseFlag.get_string_entity"></a>

#### get\_string\_entity

```python
def get_string_entity() -> str
```

Public. Returns a string representation of the flag

**Returns**:

string representation of the flag as str

<a id="argenta.command.flag.models.BaseFlag.get_name"></a>

#### get\_name

```python
def get_name() -> str
```

Public. Returns the name of the flag

**Returns**:

the name of the flag as str

<a id="argenta.command.flag.models.BaseFlag.get_prefix"></a>

#### get\_prefix

```python
def get_prefix() -> str
```

Public. Returns the prefix of the flag

**Returns**:

the prefix of the flag as str

<a id="argenta.command.flag.models.InputFlag"></a>

## InputFlag Objects

```python
class InputFlag(BaseFlag)
```

<a id="argenta.command.flag.models.InputFlag.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str,
             prefix: Literal['-', '--', '---'] = '--',
             value: str = None)
```

Public. The entity of the flag of the entered command

**Arguments**:

- `name`: the name of the input flag
- `prefix`: the prefix of the input flag
- `value`: the value of the input flag

**Returns**:

None

<a id="argenta.command.flag.models.InputFlag.get_value"></a>

#### get\_value

```python
def get_value() -> str | None
```

Public. Returns the value of the flag

**Returns**:

the value of the flag as str

<a id="argenta.command.flag.models.InputFlag.set_value"></a>

#### set\_value

```python
def set_value(value)
```

Private. Sets the value of the flag

**Arguments**:

- `value`: the fag value to set

**Returns**:

None

<a id="argenta.command.flag.models.Flag"></a>

## Flag Objects

```python
class Flag(BaseFlag)
```

<a id="argenta.command.flag.models.Flag.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str,
             prefix: Literal['-', '--', '---'] = '--',
             possible_values: list[str] | Pattern[str] | False = True) -> None
```

Public. The entity of the flag being registered for subsequent processing

**Arguments**:

- `name`: The name of the flag
- `prefix`: The prefix of the flag
- `possible_values`: The possible values of the flag, if False then the flag cannot have a value

**Returns**:

None

<a id="argenta.command.flag.models.Flag.validate_input_flag_value"></a>

#### validate\_input\_flag\_value

```python
def validate_input_flag_value(input_flag_value: str | None)
```

Private. Validates the input flag value

**Arguments**:

- `input_flag_value`: The input flag value to validate

**Returns**:

whether the entered flag is valid as bool

<a id="argenta.command.flag.models.BaseFlags"></a>

## BaseFlags Objects

```python
class BaseFlags(ABC)
```

Private. Base class for groups of flags

<a id="argenta.command.flag.models.BaseFlags.get_flags"></a>

#### get\_flags

```python
@abstractmethod
def get_flags()
```

Public. Returns a list of flags

**Returns**:

list of flags

<a id="argenta.command.flag.models.BaseFlags.add_flag"></a>

#### add\_flag

```python
@abstractmethod
def add_flag(flag: Flag | InputFlag)
```

Public. Adds a flag to the list of flags

**Arguments**:

- `flag`: flag to add

**Returns**:

None

<a id="argenta.command.flag.models.BaseFlags.add_flags"></a>

#### add\_flags

```python
@abstractmethod
def add_flags(flags: list[Flag] | list[InputFlag])
```

Public. Adds a list of flags to the list of flags

**Arguments**:

- `flags`: list of flags to add

**Returns**:

None

<a id="argenta.command.flag.models.BaseFlags.get_flag"></a>

#### get\_flag

```python
@abstractmethod
def get_flag(name: str)
```

Public. Returns the flag entity by its name or None if not found

**Arguments**:

- `name`: the name of the flag to get

**Returns**:

entity of the flag or None

<a id="argenta.command.flag"></a>

# argenta.command.flag

<a id="argenta.command.models"></a>

# argenta.command.models

<a id="argenta.command.models.BaseCommand"></a>

## BaseCommand Objects

```python
class BaseCommand()
```

<a id="argenta.command.models.BaseCommand.__init__"></a>

#### \_\_init\_\_

```python
def __init__(trigger: str) -> None
```

Private. Base class for all commands

**Arguments**:

- `trigger`: A string trigger, which, when entered by the user, indicates that the input corresponds to the command

<a id="argenta.command.models.BaseCommand.get_trigger"></a>

#### get\_trigger

```python
def get_trigger() -> str
```

Returns the trigger of the command

**Returns**:

the trigger of the command as str

<a id="argenta.command.models.Command"></a>

## Command Objects

```python
class Command(BaseCommand)
```

<a id="argenta.command.models.Command.__init__"></a>

#### \_\_init\_\_

```python
def __init__(trigger: str,
             description: str = None,
             flags: Flag | Flags = None,
             aliases: list[str] = None)
```

Public. The command that can and should be registered in the Router

**Arguments**:

- `trigger`: A string trigger, which, when entered by the user, indicates that the input corresponds to the command
- `description`: the description of the command
- `flags`: processed commands
- `aliases`: string synonyms for the main trigger

<a id="argenta.command"></a>

# argenta.command

<a id="argenta.orchestrator.argparse.arguments.models"></a>

# argenta.orchestrator.argparse.arguments.models

<a id="argenta.orchestrator.argparse.arguments.models.BaseArgument"></a>

## BaseArgument Objects

```python
class BaseArgument(ABC)
```

<a id="argenta.orchestrator.argparse.arguments.models.BaseArgument.get_string_entity"></a>

#### get\_string\_entity

```python
@abstractmethod
def get_string_entity()
```

Returns the string representation of the argument


<a id="argenta.orchestrator.argparse.arguments.models.PositionalArgument"></a>

## PositionalArgument Objects

```python
class PositionalArgument(BaseArgument)
```

<a id="argenta.orchestrator.argparse.arguments.models.PositionalArgument.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str)
```

Required argument at startup

**Arguments**:

- `name`: name of the argument, must not start with minus (-)

<a id="argenta.orchestrator.argparse.arguments.models.OptionalArgument"></a>

## OptionalArgument Objects

```python
class OptionalArgument(BaseArgument)
```

<a id="argenta.orchestrator.argparse.arguments.models.OptionalArgument.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str, prefix: Literal['-', '--', '---'] = '--')
```

Optional argument, must have the value

**Arguments**:

- `name`: name of the argument
- `prefix`: prefix of the argument

<a id="argenta.orchestrator.argparse.arguments.models.BooleanArgument"></a>

## BooleanArgument Objects

```python
class BooleanArgument(BaseArgument)
```

<a id="argenta.orchestrator.argparse.arguments.models.BooleanArgument.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str, prefix: Literal['-', '--', '---'] = '--')
```

Boolean argument, does not require a value

**Arguments**:

- `name`: name of the argument
- `prefix`: prefix of the argument

<a id="argenta.orchestrator.argparse.arguments"></a>

# argenta.orchestrator.argparse.arguments

<a id="argenta.orchestrator.argparse.entity"></a>

# argenta.orchestrator.argparse.entity

<a id="argenta.orchestrator.argparse.entity.ArgParse"></a>

## ArgParse Objects

```python
class ArgParse()
```

<a id="argenta.orchestrator.argparse.entity.ArgParse.__init__"></a>

#### \_\_init\_\_

```python
def __init__(
        processed_args: list[PositionalArgument | OptionalArgument
                             | BooleanArgument],
        name: str = 'Argenta',
        description: str = 'Argenta available arguments',
        epilog: str = 'github.com/koloideal/Argenta | made by kolo') -> None
```

Cmd argument parser and configurator at startup

**Arguments**:

- `name`: the name of the ArgParse instance
- `description`: the description of the ArgParse instance
- `epilog`: the epilog of the ArgParse instance
- `processed_args`: registered and processed arguments

<a id="argenta.orchestrator.argparse.entity.ArgParse.set_args"></a>

#### set\_args

```python
def set_args(*args: PositionalArgument | OptionalArgument | BooleanArgument)
```

Sets the arguments to be processed

**Arguments**:

- `args`: processed arguments

<a id="argenta.orchestrator.argparse.entity.ArgParse.register_args"></a>

#### register\_args

```python
def register_args()
```

Registers initialized command line arguments


<a id="argenta.orchestrator.argparse"></a>

# argenta.orchestrator.argparse

<a id="argenta.orchestrator.entity"></a>

# argenta.orchestrator.entity

<a id="argenta.orchestrator.entity.Orchestrator"></a>

## Orchestrator Objects

```python
class Orchestrator()
```

<a id="argenta.orchestrator.entity.Orchestrator.__init__"></a>

#### \_\_init\_\_

```python
def __init__(arg_parser: ArgParse = False)
```

An orchestrator and configurator that defines the behavior of an integrated system, one level higher than the App

**Arguments**:

- `arg_parser`: Cmd argument parser and configurator at startup

<a id="argenta.orchestrator.entity.Orchestrator.start_polling"></a>

#### start\_polling

```python
@staticmethod
def start_polling(app: App) -> None
```

Starting the user input processing cycle

**Arguments**:

- `app`: a running application

<a id="argenta.orchestrator.entity.Orchestrator.get_input_args"></a>

#### get\_input\_args

```python
def get_input_args() -> Namespace | None
```

Returns the arguments parsed


<a id="argenta.orchestrator"></a>

# argenta.orchestrator

<a id="argenta.router.command_handler.entity"></a>

# argenta.router.command\_handler.entity

<a id="argenta.router.command_handler"></a>

# argenta.router.command\_handler

<a id="argenta.router.defaults"></a>

# argenta.router.defaults

<a id="argenta.router.entity"></a>

# argenta.router.entity

<a id="argenta.router.exceptions"></a>

# argenta.router.exceptions

<a id="argenta.router"></a>

# argenta.router

