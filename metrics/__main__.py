from argenta import App, Command, Orchestrator
from metrics.handlers import router

app = App(initial_message="metrics", exit_command=Command("exit", aliases=["quit"]))

app.include_router(router)
orchestrator = Orchestrator()


def main() -> None:
    app.set_description_message_pattern(
        lambda command, description: (
            f"[bold cyan]▸[/bold cyan] [bold white]{command}[/bold white] [dim]│[/dim] "
            f"[yellow italic]{description}[/yellow italic]"
        )
    )
    orchestrator.run_repl(app)


if __name__ == "__main__":
    main()
