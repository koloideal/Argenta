from argenta import App, Orchestrator
from argenta.orchestrator.argparser import ArgParser, BooleanArgument

arg_parser = ArgParser(
    processed_args=[
        BooleanArgument("dev")
    ]
)
orchestrator = Orchestrator(
    arg_parser=arg_parser,
)

if __name__ == "__main__":
    if arg_parser.parsed_argspace.get_by_name("dev"):
        orchestrator.run_repl(App(initial_message="ArgentaDev"))
    else:
        orchestrator.run_repl(App())
