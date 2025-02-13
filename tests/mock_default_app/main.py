from pprint import pprint
from tests.mock_default_app.handlers.routers import work_router, settings_router
from argenta.app.entity import App


app: App = App(ignore_command_register=False,
               line_separate='\n-------------------------------\n')


def main():
    app.include_router(work_router, is_main=True)
    app.include_router(settings_router)

    app.start_polling()

if __name__ == "__main__":
    main()
