import os
import readline
from typing import Never, Optional


class AutoCompleter:
    def __init__(
        self, history_filename: Optional[str] = None, autocomplete_button: str = "tab"
    ) -> None:
        """
        Public. Configures and implements auto-completion of input command
        :param history_filename: the name of the file for saving the history of the autocompleter
        :param autocomplete_button: the button for auto-completion
        :return: None
        """
        self.history_filename = history_filename
        self.autocomplete_button = autocomplete_button

    def _complete(self, text: str, state: int) -> Optional[str]:
        """
        Private. Auto-completion function
        :param text: part of the command being entered
        :param state: the current cursor position is relative to the beginning of the line
        :return: the desired candidate as str or None
        """
        matches: list[str] = sorted(
            cmd for cmd in self.get_history_items() if cmd.startswith(text)
        )
        if len(matches) > 1:
            common_prefix = matches[0]
            for match in matches[1:]:
                i = 0
                while (
                    i < len(common_prefix)
                    and i < len(match)
                    and common_prefix[i] == match[i]
                ):
                    i += 1
                common_prefix = common_prefix[:i]
            if state == 0:
                readline.insert_text(common_prefix[len(text) :]) # type: ignore
                readline.redisplay() # type: ignore
            return None
        elif len(matches) == 1:
            return matches[0] if state == 0 else None
        else:
            return None

    def initial_setup(self, all_commands: list[str]) -> None:
        """
        Private. Initial setup function
        :param all_commands: Registered commands for adding them to the autocomplete history
        :return: None
        """
        if self.history_filename:
            if os.path.exists(self.history_filename):
                readline.read_history_file(self.history_filename) # type: ignore
            else:
                for line in all_commands:
                    readline.add_history(line) # type: ignore

        readline.set_completer(self._complete) # type: ignore
        readline.set_completer_delims(readline.get_completer_delims().replace(" ", "")) # type: ignore
        readline.parse_and_bind(f"{self.autocomplete_button}: complete") # type: ignore

    def exit_setup(self, all_commands: list[str]) -> None:
        """
        Private. Exit setup function
        :return: None
        """
        if self.history_filename:
            readline.write_history_file(self.history_filename) # type: ignore
            with open(self.history_filename, "r") as history_file:
                raw_history = history_file.read()
            pretty_history: list[str] = []
            for line in set(raw_history.strip().split("\n")):
                if line.split()[0] in all_commands:
                    pretty_history.append(line)
            with open(self.history_filename, "w") as history_file:
                history_file.write("\n".join(pretty_history))

    @staticmethod
    def get_history_items() -> list[str] | list[Never]:
        """
        Private. Returns a list of all commands entered by the user
        :return: all commands entered by the user as list[str] | list[Never]
        """
        return [
            readline.get_history_item(i) # type: ignore
            for i in range(1, readline.get_current_history_length() + 1) # type: ignore
        ]
