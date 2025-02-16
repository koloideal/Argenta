import re
from pprint import pprint


class CommandParseError(Exception):
    pass

def parse_command(command: str) -> dict:
    pattern = re.compile(r"""
        (?P<command>^\S+)                       
        |                                      
        (?P<arg_prefix>-{1,3})(?P<arg>\w+)       
        |                                      
        (?P<value>\S+)                   
    """, re.VERBOSE)

    tokens = pattern.findall(command)
    if not tokens:
        raise CommandParseError("Invalid command format")

    result = {}
    args = {}
    current_arg = None

    for token in tokens:
        command_name, arg_prefix, arg_name, value = token

        if command_name:
            if "command" in result:
                raise CommandParseError("Multiple command names found")
            result["command"] = command_name

        elif arg_name:
            if current_arg:
                raise CommandParseError(f"Argument {current_arg} has no value")
            current_arg = f"{arg_prefix}{arg_name}"

        elif value:
            if not current_arg:
                raise CommandParseError(f"Unexpected value: {value}")
            args[current_arg] = value
            current_arg = None

    if current_arg:
        raise CommandParseError(f"Argument {current_arg} has no value")

    result["args"] = args
    return result


command_str = "run"
parsed = (command_str)
pprint(parsed)
