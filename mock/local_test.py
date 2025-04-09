import readline
import os

HISTORY_FILENAME = 'completer.hist'


def get_history_items():
    return [readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)]


class HistoryCompleter:

    def __init__(self):
        self.matches = []
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            history_values = get_history_items()
            if text:
                self.matches = sorted(h
                                      for h in history_values
                                      if h and h.startswith(text))
            else:
                self.matches = []
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def inputing():
    if os.path.exists(HISTORY_FILENAME):
        readline.read_history_file(HISTORY_FILENAME)
    print(f'Максимальная длина файла истории: {readline.get_history_length()}')
    print(f'История запуска:{get_history_items()}')
    try:
        while True:
            line = input('!("stop" to quit) Ввод текста: => ')
            if line == 'stop':
                break
            if line:
                print(f'Добавление "{line}" в файл истории.')
    finally:
        print(f'Конец записи истории: {get_history_items()}')
        readline.write_history_file(HISTORY_FILENAME)


# Регистрация класса 'HistoryCompleter'
readline.set_completer(HistoryCompleter().complete)

# Регистрация клавиши `tab` для автодополнения
readline.parse_and_bind('tab: complete')

# Запрос текста
inputing()