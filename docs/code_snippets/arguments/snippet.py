from argenta.orchestrator.argparser import ArgParser, ValueArgument

# Create arguments
config_arg = ValueArgument(
    "config",
    help="Path to configuration file",
    default="config.yaml"
)

log_level_arg = ValueArgument(
    "log-level",
    help="Logging level",
    possible_values=["DEBUG", "INFO", "WARNING", "ERROR"],
    default="INFO"
)

host_arg = ValueArgument(
    "host",
    help="Server host address",
    is_required=True
)

# Register in ArgParser
parser = ArgParser(
    processed_args=[config_arg, log_level_arg, host_arg],
    name="MyApp",
    description="My application with CLI arguments"
)