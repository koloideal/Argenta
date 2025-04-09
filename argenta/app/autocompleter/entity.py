import readline
import os



class AutoCompleter:
    def __init__(self, history_filename: str = False, autocomplete_button: str = 'tab'):
        self.history_filename = history_filename
        self.autocomplete_button = autocomplete_button
        self.matches = []

    def complete(self, text, state):
        matches = sorted(cmd for cmd in self.get_history_items() if cmd.startswith(text))
        if len(matches) > 1:
            common_prefix = matches[0]
            for match in matches[1:]:
                i = 0
                while i < len(common_prefix) and i < len(match) and common_prefix[i] == match[i]:
                    i += 1
                common_prefix = common_prefix[:i]
            if state == 0:
                readline.insert_text(common_prefix[len(text):])
                readline.redisplay()
            return None
        elif len(matches) == 1:
            return matches[0] if state == 0 else None
        else:
            return None

    def initial_setup(self):
        if self.history_filename:
            if os.path.exists(self.history_filename):
                readline.read_history_file(self.history_filename)
        readline.set_completer(self.complete)
        readline.set_completer_delims(readline.get_completer_delims().replace(' ', ''))
        readline.parse_and_bind(f'{self.autocomplete_button}: complete')

    def exit_setup(self):
        if self.history_filename:
            readline.write_history_file(self.history_filename)

    @staticmethod
    def get_history_items():
        return [readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)]

