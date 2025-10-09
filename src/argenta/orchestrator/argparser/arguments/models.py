class BaseArgument:
    """
    Private. Base class for all arguments
    """
    def __init__(self, name: str, *,
                       help: str,
                       is_required: bool,
                       is_deprecated: bool):
        """
        Public. Boolean argument, does not require a value
        :param name: name of the argument
        :param help: help message for the argument
        :param is_required: whether the argument is required
        :param is_deprecated: whether the argument is deprecated
        """
        self.name: str = name
        self.help: str = help
        self.is_required: bool = is_required
        self.is_deprecated: bool = is_deprecated


class RequiredArgument(BaseArgument):
    def __init__(self, name: str, *,
                       help: str = "Help for required argument",
                       default: str | None = None,
                       possible_values: list[str] | None = None,
                       is_required: bool = True,
                       is_deprecated: bool = False):
        """
        Public. Required argument at startup
        :param name: name of the argument, must not start with minus (-)
        :param help: help message for the argument
        :param default: default value for the argument
        :param possible_values: list of possible values for the argument
        :param is_required: whether the argument is required
        :param is_deprecated: whether the argument is deprecated
        """
        self.default: str | None = default
        self.possible_values: list[str] | None = possible_values
        self.action: str = "store"
        super().__init__(name, help=help, is_required=is_required, is_deprecated=is_deprecated)


class ValueArgument(BaseArgument):
    def __init__(self, name: str, *,
                       help: str = "Help message for the value argument", 
                       possible_values: list[str] | None = None,
                       default: str | None = None,
                       is_required: bool = False,
                       is_deprecated: bool = False):
        """
        Public. Value argument, must have the value
        :param name: name of the argument
        :param help: help message for the argument
        :param possible_values: list of possible values for the argument
        :param default: default value for the argument
        :param is_required: whether the argument is required
        :param is_deprecated: whether the argument is deprecated
        """
        self.default: str | None = default
        self.possible_values: list[str] | None = possible_values
        self.action: str = "store"
        super().__init__(name, help=help, is_required=is_required, is_deprecated=is_deprecated)


class BooleanArgument(BaseArgument):
    def __init__(self, name: str, *,
                       help: str = "Help message for the boolean argument",
                       is_required: bool = False,
                       is_deprecated: bool = False):
        """
        Public. Boolean argument, does not require a value
        :param name: name of the argument
        :param help: help message for the argument
        :param is_required: whether the argument is required
        :param is_deprecated: whether the argument is deprecated
        """
        self.action: str = "store_true"
        super().__init__(name, help=help, is_required=is_required, is_deprecated=is_deprecated)


class InputArgument:
    def __init__(self, name: str,
                       value: str | None,
                       founder_class: type[BaseArgument]) -> None:
        self.name: str = name
        self.value: str | None = value
        self.founder_class: type[BaseArgument] = founder_class
    
    def __str__(self) -> str:
        return f"{self.name}={self.value}" 
