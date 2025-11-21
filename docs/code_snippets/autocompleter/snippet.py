from argenta import App
from argenta.app import AutoCompleter

# Setting up autocompletion with saving history to a file
my_autocompleter = AutoCompleter(history_filename="argenta_history.txt")

# Passing the configured autocompleter to the application
app = App(autocompleter=my_autocompleter)

# ... the rest of the application logic
