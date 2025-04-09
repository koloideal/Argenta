import readline
import os



class Autocompleter:
    def __init__(self, history_filename: str = './completer.hist', autocomplete_button: str = 'tab'):
        self.history_filename = history_filename
        self.autocomplete_button = autocomplete_button
        self.matches = []

    def complete(self, text, state):
        if state == 0:
            history_values = self.get_history_items()
            if text:
                self.matches = sorted(h for h in history_values if h and h.startswith(text))
            else:
                self.matches = []
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

    def initial_setup(self):
        if os.path.exists(self.history_filename):
            readline.read_history_file(self.history_filename)
        readline.set_completer(self.complete)
        readline.parse_and_bind(f'{self.autocomplete_button}: complete')

    def write_command_to_history(self):
        readline.write_history_file(self.history_filename)

    @staticmethod
    def get_history_items():
        return [readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)]



def inputting():
    autocompleter = Autocompleter()
    autocompleter.initial_setup()
    print(f'Максимальная длина файла истории: {readline.get_history_length()}')
    print(f'История запуска:{autocompleter.get_history_items()}')
    while True:
        line = input('\n!("stop" to quit) Ввод текста: => ')
        if line == 'stop':
            print(f'Конец записи истории: {autocompleter.get_history_items()}')
            autocompleter.write_command_to_history()
            break


inputting()





