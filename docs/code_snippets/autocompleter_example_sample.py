from argenta import App
from argenta.app.autocompleter import AutoCompleter

# Настройка автодополнения с сохранением истории в файл
my_autocompleter = AutoCompleter(history_filename="argenta_history.txt")

# Передача настроенного автокомплитера в приложение
app = App(autocompleter=my_autocompleter)

# ... остальная логика приложения