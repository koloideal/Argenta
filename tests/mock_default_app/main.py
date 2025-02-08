from tests.mock_default_app.handlers.routers import work_router, settings_router
from argenta.app.entity import App
from art import text2art


app: App = App()


def main():
    app.include_router(work_router, is_main=True)
    app.include_router(settings_router)

    app.start_polling()

if __name__ == "__main__":
    main()
