from mock.mock_app.handlers.routers import work_router, settings_router

from argenta.app import App
from argenta.app.defaults import PredeterminedMessages
from argenta.app.dividing_line import DynamicDividingLine
from argenta.app.autocompleter import AutoCompleter


autocompleter = AutoCompleter('./mock/.hist')
app: App = App(dividing_line=DynamicDividingLine(),
               autocompleter=autocompleter)


def main():
    app.include_routers(work_router, settings_router)

    app.add_message_on_startup(PredeterminedMessages.USAGE)
    app.add_message_on_startup(PredeterminedMessages.AUTOCOMPLETE)
    app.add_message_on_startup(PredeterminedMessages.HELP)

    app.start_polling()

if __name__ == "__main__":
    main()
