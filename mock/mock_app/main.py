from mock.mock_app.handlers.routers import work_router, settings_router

from argenta.app import App
from argenta.app.defaults import PredeterminedMessages


app: App = App()


def main():
    app.include_routers(work_router, settings_router)

    app.add_message_on_startup(PredeterminedMessages.USAGE)
    app.add_message_on_startup(PredeterminedMessages.HELP + '\n\n')

    app.start_polling()

if __name__ == "__main__":
    main()
