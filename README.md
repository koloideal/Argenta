# Argenta

### Python library for creating TUI

---

<details>

<summary>Contents</summary>
   
- [**Installing**](#installing) 
- [**Quick Start**](#quick-start) 
- [**Documentation**](#documentation)
   - [**App** Objects](#app-objects)
      - [set\_description\_message\_pattern](#set\_description\_message\_pattern)  
      - [set\_invalid\_input\_flags\_handler](#set\_invalid\_input\_flags\_handler)    
      - [set\_repeated\_input\_flags\_handler](#set\_repeated\_input\_flags\_handler)   
      - [set\_unknown\_command\_handler](#set\_unknown\_command\_handler)  
      - [set\_empty\_command\_handler](#set\_empty\_command\_handler)  
      - [set\_exit\_command\_handler](#set\_exit\_command\_handler)  
      - [run\_polling](#run\_polling)  
      - [include\_router](#include\_router)  
      - [include\_routers](#include\_routers)  
      - [add\_message\_on\_startup](#add\_message\_on\_startup)  
  - [**AutoCompleter** Objects](#autocompleter-objects) 
  - [**PredefinedMessages** Objects](#predefinedmessages-objects) 
  - [**StaticDividingLine** Objects](#staticdividingline-objects)
      - [get\_full\_static\_line](#get\_full\_static\_line)  
  - [**DynamicDividingLine** Objects](#dynamicdividingline-objects) 
      - [get\_full\_dynamic\_line](#get\_full\_dynamic\_line)  
  - [**NoRegisteredHandlersException** Objects](#noregisteredhandlersexception-objects)  
  - [**UnprocessedInputFlagException** Objects](#unprocessedinputflagexception-objects)  
  - [**RepeatedInputFlagsException** Objects](#repeatedinputflagsexception-objects)  
  - [**EmptyInputCommandException** Objects](#emptyinputcommandexception-objects)  
  - [**PredefinedFlags** Objects](#predefinedflags-objects)  
  - [**InputFlag** Objects](#inputflag-objects)  
      - [get\_value](#get\_value)  
  - [**Flag** Objects](#flag-objects)
  - [**Flags** Objects](#flags-objects)
      - [get\_flags](#get\_flags)  
      - [add\_flag](#add\_flag)  
      - [add\_flags](#add\_flags)  
      - [get\_flag](#get\_flag)  
  - [**InputFlags** Objects](#inputflags-objects) 
      - [get\_flags](#get\_flags)  
      - [add\_flag](#add\_flag)  
      - [add\_flags](#add\_flags)  
      - [get\_flag](#get\_flag)  
  - [**Command** Objects](#command-objects)  
  - [**PositionalArgument** Objects](#positionalargument-objects) 
  - [**OptionalArgument** Objects](#optionalargument-objects) 
  - [**BooleanArgument** Objects](#booleanargument-objects) 
  - [**ArgParse** Objects](#argparse-objects) 
      - [set\_args](#set\_args)  
  - [**Orchestrator** Objects](#orchestrator-objects) 
      - [start\_polling](#start\_polling)  
      - [get\_input\_args](#get\_input\_args)  
  - [**Router** Objects](#router-objects) 
      - [@command](#@command)  
      - [set\_invalid\_input\_flag\_handler](#set\_invalid\_input\_flag\_handler)  
      - [input\_command\_handler](#input\_command\_handler)  
      - [set\_command\_register\_ignore](#set\_command\_register\_ignore)  
      - [get\_triggers](#get\_triggers)  
      - [get\_aliases](#get\_aliases)  
      - [get\_title](#get\_title)  
      - [set\_title](#set\_title)  
  - [**RepeatedFlagNameException** Objects](#repeatedflagnameexception-objects) 
  - [**TooManyTransferredArgsException** Objects](#toomanytransferredargsexception-objects) 
  - [**RequiredArgumentNotPassedException** Objects](#requiredargumentnotpassedexception-objects) 
  - [**IncorrectNumberOfHandlerArgsException** Objects](#incorrectnumberofhandlerargsexception-objects) 
  - [**TriggerContainSpacesException** Objects](#triggercontainspacesexception-objects)
- [**Tests**](#tests)
</details>  

---

![preview](https://github.com/koloideal/Argenta/blob/kolo/imgs/mock_app_preview4.png?raw=True)  
An example of the TUI appearance

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
Example TUI with a command that has processed flags

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

# Documentation

<a id="argenta.app.models"></a>

# `.app`

<a id="argenta.app.models.App"></a>

## App Objects

```python
class App(BaseApp)
```

<a id="argenta.app.models.App.__init__"></a>

#### \_\_init\_\_

```python
def __init__(prompt: str = 'What do you want to do?',
             initial_message: str = 'Argenta',
             farewell_message: str = 'See you',
             exit_command: Command = Command('Q', 'Exit command'),
             system_router_title: str | None = 'System points:',
             ignore_command_register: bool = True,
             dividing_line: StaticDividingLine | DynamicDividingLine = StaticDividingLine(),
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

`None`

---

<a id="argenta.app.models.BaseApp.set_description_message_pattern"></a>

#### set\_description\_message\_pattern

```python
def set_description_message_pattern(pattern: Callable[[str, str], str]) -> None
```

Public. Sets the output pattern of the available commands

**Arguments**:

- `pattern`: output pattern of the available commands

**Returns**:

`None`

---

<a id="argenta.app.models.BaseApp.set_invalid_input_flags_handler"></a>

#### set\_invalid\_input\_flags\_handler

```python
def set_invalid_input_flags_handler(handler: Callable[[str], None]) -> None
```

Public. Sets the handler for incorrect flags when entering a command

**Arguments**:

- `handler`: handler for incorrect flags when entering a command

**Returns**:

`None`

---

<a id="argenta.app.models.BaseApp.set_repeated_input_flags_handler"></a>

#### set\_repeated\_input\_flags\_handler

```python
def set_repeated_input_flags_handler(handler: Callable[[str], None]) -> None
```

Public. Sets the handler for repeated flags when entering a command

**Arguments**:

- `handler`: handler for repeated flags when entering a command

**Returns**:

`None`

---

<a id="argenta.app.models.BaseApp.set_unknown_command_handler"></a>

#### set\_unknown\_command\_handler

```python
def set_unknown_command_handler(handler: Callable[[str], None]) -> None
```

Public. Sets the handler for unknown commands when entering a command

**Arguments**:

- `handler`: handler for unknown commands when entering a command

**Returns**:

`None`

---

<a id="argenta.app.models.BaseApp.set_empty_command_handler"></a>

#### set\_empty\_command\_handler

```python
def set_empty_command_handler(handler: Callable[[], None]) -> None
```

Public. Sets the handler for empty commands when entering a command

**Arguments**:

- `handler`: handler for empty commands when entering a command

**Returns**:

`None`

---

<a id="argenta.app.models.BaseApp.set_exit_command_handler"></a>

#### set\_exit\_command\_handler

```python
def set_exit_command_handler(handler: Callable[[], None]) -> None
```

Public. Sets the handler for exit command when entering a command

**Arguments**:

- `handler`: handler for exit command when entering a command

**Returns**:

`None`

---

<a id="argenta.app.models.App.include_router"></a>

#### include\_router

```python
def include_router(router: Router) -> None
```

Public. Registers the router in the application

**Arguments**:

- `router`: registered router

**Returns**:

`None`

---

<a id="argenta.app.models.App.include_routers"></a>

#### include\_routers

```python
def include_routers(*routers: Router) -> None
```

Public. Registers the routers in the application

**Arguments**:

- `routers`: registered routers

**Returns**:

`None`

---

<a id="argenta.app.models.App.add_message_on_startup"></a>

#### add\_message\_on\_startup

```python
def add_message_on_startup(message: str) -> None
```

Public. Adds a message that will be displayed when the application is launched

**Arguments**:

- `message`: the message being added

**Returns**:

`None`

---

<a id="argenta.app.autocompleter.entity"></a>

# `.app.autocompleter`

<a id="argenta.app.autocompleter.entity.AutoCompleter"></a>

## AutoCompleter Objects

```python
class AutoCompleter()
```

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

`None`

---

<a id="argenta.app.defaults"></a>

# `.app.defaults`

<a id="argenta.app.defaults.PredefinedMessages"></a>

## PredefinedMessages Objects

```python
@dataclass
class PredefinedMessages()
```

Public. A dataclass with predetermined messages for quick use

---

<a id="argenta.app.dividing_line.models"></a>

# `.app.dividing_line`

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

`None`

---

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

`None`

---

<a id="argenta.app.exceptions"></a>

# `.app.exceptions`

<a id="argenta.app.exceptions.NoRegisteredHandlersException"></a>

## NoRegisteredHandlersException Objects

```python
class NoRegisteredHandlersException(Exception)
```

The router has no registered handlers

---

<a id="argenta.command.exceptions"></a>

# `.command.exceptions`

<a id="argenta.command.exceptions.BaseInputCommandException"></a>

## UnprocessedInputFlagException Objects

```python
class UnprocessedInputFlagException(BaseInputCommandException)
```

Private. Raised when an unprocessed input flag is detected

---

<a id="argenta.command.exceptions.RepeatedInputFlagsException"></a>

## RepeatedInputFlagsException Objects

```python
class RepeatedInputFlagsException(BaseInputCommandException)
```

Private. Raised when repeated input flags are detected

---

<a id="argenta.command.exceptions.EmptyInputCommandException"></a>

## EmptyInputCommandException Objects

```python
class EmptyInputCommandException(BaseInputCommandException)
```

Private. Raised when an empty input command is detected

---

<a id="argenta.command.flag.defaults"></a>

# `.command.flag.defaults`

<a id="argenta.command.flag.defaults.PredefinedFlags"></a>

## PredefinedFlags Objects

```python
@dataclass
class PredefinedFlags()
```

Public. A dataclass with predefined flags and most frequently used flags for quick use

---

<a id="argenta.command.flag.models"></a>

# `.command.flag`

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

`None`

---

<a id="argenta.command.flag.models.InputFlag.get_value"></a>

#### get\_value

```python
def get_value() -> str | None
```

Public. Returns the value of the flag

**Returns**:

the value of the flag as str

---

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

`None`

---

<a id="argenta/command/flag/models.Flags"></a>

## Flags Objects

```python
class Flags(BaseFlags)
```

<a id="argenta/command/flag/models.Flags.__init__"></a>

#### \_\_init\_\_

```python
def __init__(*flags: Flag)
```

Public. A model that combines the registered flags

**Arguments**:

- `flags`: the flags that will be registered

**Returns**:

`None`

---
<a id="argenta.command.flag.models.BaseFlags.get_flags"></a>

#### get\_flags

```python
def get_flags() -> list[Flag]
```

Public. Returns a list of flags

**Returns**:

list of flags as list[Flag]

---

<a id="argenta.command.flag.models.BaseFlags.add_flag"></a>

#### add\_flag

```python
def add_flag(flag: Flag) -> None
```

Public. Adds a flag to the list of flags

**Arguments**:

- `flag`: flag to add

**Returns**:

`None`

---

<a id="argenta.command.flag.models.BaseFlags.add_flags"></a>

#### add\_flags

```python
def add_flags(flags: list[Flag]) -> None
```

Public. Adds a list of flags to the list of flags

**Arguments**:

- `flags`: list of flags to add

**Returns**:

`None`

---

<a id="argenta.command.flag.models.BaseFlags.get_flag"></a>

#### get\_flag

```python
def get_flag(name: str) -> Flag | None
```

Public. Returns the flag entity by its name or None if not found

**Arguments**:

- `name`: the name of the flag to get

**Returns**:

entity of the flag or None

---

<a id="argenta/command/flag/models.InputFlags"></a>

## InputFlags Objects

```python
class InputFlags(BaseFlags)
```

<a id="argenta/command/flag/models.InputFlags.__init__"></a>

#### \_\_init\_\_

```python
def __init__(*flags: InputFlag)
```

Public. A model that combines the input flags of the input command

**Arguments**:

- `flags`: all input flags

**Returns**:

`None`

---

<a id="argenta.command.flag.models.BaseFlags.get_flags"></a>

#### get\_flags

```python
def get_flags() -> list[InputFlag]
```

Public. Returns a list of flags

**Returns**:

list of flags

---

<a id="argenta.command.flag.models.BaseFlags.add_flag"></a>

#### add\_flag

```python
def add_flag(flag: InputFlag) -> None
```

Public. Adds a flag to the list of flags

**Arguments**:

- `flag`: flag to add

**Returns**:

`None`

---

<a id="argenta.command.flag.models.BaseFlags.add_flags"></a>

#### add\_flags

```python
def add_flags(flags: list[InputFlag]) -> None
```

Public. Adds a list of flags to the list of flags

**Arguments**:

- `flags`: list of flags to add

**Returns**:

`None`

---

<a id="argenta.command.flag.models.BaseFlags.get_flag"></a>

#### get\_flag

```python
def get_flag(name: str) -> InputFlag
```

Public. Returns the flag entity by its name or None if not found

**Arguments**:

- `name`: the name of the flag to get

**Returns**:

entity of the flag or None

---

<a id="argenta.command.models"></a>

# `.command.models`

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

---

<a id="argenta.orchestrator.argparse.arguments.models"></a>

# `.orchestrator.argparse.arguments`

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

Public. Required argument at startup

**Arguments**:

- `name`: name of the argument, must not start with minus (-)

---

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

Public. Optional argument, must have the value

**Arguments**:

- `name`: name of the argument
- `prefix`: prefix of the argument

---

<a id="argenta.orchestrator.argparse.arguments.models.BooleanArgument"></a>

## BooleanArgument Objects

```python
class BooleanArgument(BaseArgument)
```

<a id="argenta.orchestrator.argparse.arguments.models.BooleanArgument.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str,
             prefix: Literal['-', '--', '---'] = '--')
```

Public. Boolean argument, does not require a value

**Arguments**:

- `name`: name of the argument
- `prefix`: prefix of the argument

---

<a id="argenta.orchestrator.argparse.entity"></a>

# `.orchestrator.argparser`

<a id="argenta.orchestrator.argparse.entity.ArgParser"></a>

## ArgParse Objects

```python
class ArgParse()
```

<a id="argenta.orchestrator.argparse.entity.ArgParse.__init__"></a>

#### \_\_init\_\_

```python
def __init__(processed_args: list[PositionalArgument | OptionalArgument | BooleanArgument],
             name: str = 'Argenta',
             description: str = 'Argenta available arguments',
             epilog: str = 'github.com/koloideal/Argenta | made by kolo') -> None
```

Public. Cmd argument parser and configurator at startup

**Arguments**:

- `name`: the name of the ArgParse instance
- `description`: the description of the ArgParse instance
- `epilog`: the epilog of the ArgParse instance
- `processed_args`: registered and processed arguments

---

<a id="argenta.orchestrator.argparse.entity.ArgParse.set_args"></a>

#### set\_args

```python
def set_args(*args: PositionalArgument | OptionalArgument | BooleanArgument) -> None
```

Public. Sets the arguments to be processed

**Arguments**:

- `args`: processed arguments

**Returns**:

`None`

---

# `.orchestrator`

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

Public. An orchestrator and configurator that defines the behavior of an integrated system, one level higher than the App

**Arguments**:

- `arg_parser`: Cmd argument parser and configurator at startup

**Returns**:

`None`

---

<a id="argenta.orchestrator.entity.Orchestrator.start_polling"></a>

#### start\_polling

```python
@staticmethod
def start_polling(app: App) -> None
```

Public. Starting the user input processing cycle

**Arguments**:

- `app`: a running application

**Returns**:

`None`

---

<a id="argenta.orchestrator.entity.Orchestrator.get_input_args"></a>

#### get\_input\_args

```python
def get_input_args() -> Namespace | None
```

Public. Returns the arguments parsed

**Returns**:

`None`

---

<a id="argenta.router.entity"></a>

# `.router`

<a id="argenta.router.entity.Router"></a>

## Router Objects

```python
class Router()
```

<a id="argenta.router.entity.Router.__init__"></a>

#### \_\_init\_\_

```python
def __init__(title: str = None)
```

Public. Directly configures and manages handlers

**Arguments**:

- `title`: the title of the router, displayed when displaying the available commands

**Returns**:

`None`

---

<a id="argenta.router.entity.Router.command"></a>

#### @command

```python
def command(command: Command) -> Callable
```

Public. Registers handler

**Arguments**:

- `command`: Registered command

**Returns**:

decorated handler as Callable[[Any], Any]

---

<a id="argenta.router.entity.Router.set_invalid_input_flag_handler"></a>

#### set\_invalid\_input\_flag\_handler

```python
def set_invalid_input_flag_handler(func) -> None
```

Public. Registers handler for invalid input flag

**Arguments**:

- `func`: registered handler

**Returns**:

`None`

---

<a id="argenta.router.entity.Router.get_triggers"></a>

#### get\_triggers

```python
def get_triggers() -> list[str]
```

Public. Gets registered triggers

**Returns**:

registered in router triggers as list[str]

---

<a id="argenta.router.entity.Router.get_aliases"></a>

#### get\_aliases

```python
def get_aliases() -> list[str]
```

Public. Gets registered aliases

**Returns**:

registered in router aliases as list[str]

---

<a id="argenta.router.entity.Router.get_title"></a>

#### get\_title

```python
def get_title() -> str | None
```

Public. Gets title of the router

**Returns**:

the title of the router as str or None

---

<a id="argenta.router.entity.Router.set_title"></a>

#### set\_title

```python
def set_title(title: str) -> None
```

Public. Sets the title of the router

**Arguments**:

- `title`: title that will be setted

**Returns**:

`None`

---

<a id="argenta.router.exceptions"></a>

# `.router.exceptions`

<a id="argenta.router.exceptions.RepeatedFlagNameException"></a>

## RepeatedFlagNameException Objects

```python
class RepeatedFlagNameException(Exception)
```

Private. Raised when a repeated flag name is registered

---

<a id="argenta.router.exceptions.TooManyTransferredArgsException"></a>

## TooManyTransferredArgsException Objects

```python
class TooManyTransferredArgsException(Exception)
```

Private. Raised when too many arguments are passed

---

<a id="argenta.router.exceptions.RequiredArgumentNotPassedException"></a>

## RequiredArgumentNotPassedException Objects

```python
class RequiredArgumentNotPassedException(Exception)
```

Private. Raised when a required argument is not passed

---

<a id="argenta.router.exceptions.IncorrectNumberOfHandlerArgsException"></a>

## IncorrectNumberOfHandlerArgsException Objects

```python
class IncorrectNumberOfHandlerArgsException(Exception)
```

Private. Raised when incorrect number of arguments are passed

---

<a id="argenta.router.exceptions.TriggerContainSpacesException"></a>

## TriggerContainSpacesException Objects

```python
class TriggerContainSpacesException(Exception)
```

Private. Raised when there is a space in the trigger being registered

<a id="argenta.router"></a>

---

# Tests

Run tests:

```bash
python -m unittest discover
```
or
```bash
python -m unittest discover -v
```

---

# made by kolo `MIT` `2025`

