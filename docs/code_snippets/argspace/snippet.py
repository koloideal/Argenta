from argenta import App, Orchestrator
from argenta.orchestrator.argparser import ArgParser, ValueArgument

arguments = [
    ValueArgument("host", help="Server host", is_required=True),
    ValueArgument("port", help="Server port", is_required=True),
]

argparser = ArgParser(processed_args=arguments, name="WebServer", description="Simple web server")

app = App()
orchestrator = Orchestrator(argparser)


def main():
    argspace = argparser.parsed_argspace

    host = argspace.get_by_name("host")
    port = argspace.get_by_name("port")

    print("Server configuration:")
    print(f"  Host: {host.value}")
    print(f"  Port: {port.value}")

    orchestrator.run_repl(app)


if __name__ == "__main__":
    main()
