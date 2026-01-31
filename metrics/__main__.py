from argenta import App, Orchestrator
from argenta.app import DynamicDividingLine
from .handlers import router


app = App(initial_message="metrics", dividing_line=DynamicDividingLine('~'), override_system_messages=True)
orchestrator = Orchestrator()


def main() -> None:
    app.include_router(router)
    app.set_description_message_pattern(
        lambda command, description: f'[bold cyan]▸[/bold cyan] [bold white]{command}[/bold white] [dim]│[/dim] [yellow italic]{description}[/yellow italic]'
    )
    orchestrator.start_polling(app)


if __name__ == "__main__":
    main()
