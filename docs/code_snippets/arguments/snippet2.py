from argenta.orchestrator.argparser import ArgParser, BooleanArgument

# Создание булевых аргументов
verbose_arg = BooleanArgument(
    "verbose",
    help="Enable verbose output"
)

debug_arg = BooleanArgument(
    "debug",
    help="Enable debug mode"
)

no_cache_arg = BooleanArgument(
    "no-cache",
    help="Disable caching"
)

# Регистрация в ArgParser
parser = ArgParser(
    processed_args=[verbose_arg, debug_arg, no_cache_arg],
    name="MyApp"
)