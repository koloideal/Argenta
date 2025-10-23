from argenta import Orchestrator, App
from argenta.orchestrator.argparser import BooleanArgument, ArgParser

arg_parser = ArgParser(processed_args=[BooleanArgument('config')])
orchestrator = Orchestrator(
    arg_parser=arg_parser,
)

if __name__ == "__main__":
    orchestrator.start_polling(App())