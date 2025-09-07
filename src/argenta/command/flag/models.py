from enum import Enum
from typing import Literal, Pattern



class PossibleValues(Enum):
    NEITHER = 'NEITHER'
    ALL = 'ALL'


class ValidationStatus(Enum):
    VALID = 'VALID'
    INVALID = 'INVALID'
    UNDEFINED = 'UNDEFINED'


class Flag:
    def __init__(
        self, name: str, *, 
        prefix: Literal["-", "--", "---"] = "--",
        possible_values: list[str] | Pattern[str] | PossibleValues = PossibleValues.ALL,
    ) -> None:
        """
        Public. The entity of the flag being registered for subsequent processing
        :param name: The name of the flag
        :param prefix: The prefix of the flag
        :param possible_values: The possible values of the flag, if False then the flag cannot have a value
        :return: None
        """
        self._name = name
        self._prefix = prefix
        self._possible_values = possible_values

    def validate_input_flag_value(self, input_flag_value: str | None) -> bool:
        """
        Private. Validates the input flag value
        :param input_flag_value: The input flag value to validate
        :return: whether the entered flag is valid as bool
        """
        if self._possible_values == PossibleValues.NEITHER:
            if input_flag_value is None:
                return True
            else:
                return False
            
        elif isinstance(self._possible_values, Pattern):
            if isinstance(input_flag_value, str):
                is_valid = bool(self._possible_values.match(input_flag_value))
                if bool(is_valid):
                    return True
                else:
                    return False
            else:
                return False

        elif isinstance(self._possible_values, list):
            if input_flag_value in self._possible_values:
                return True
            else:
                return False
        else:
            return True
    
    @property
    def string_entity(self) -> str:
        """
        Public. Returns a string representation of the flag
        :return: string representation of the flag as str
        """
        string_entity: str = self._prefix + self._name
        return string_entity

    @property
    def name(self) -> str:
        """
        Public. Returns the name of the flag
        :return: the name of the flag as str
        """
        return self._name

    @property
    def prefix(self) -> str:
        """
        Public. Returns the prefix of the flag
        :return: the prefix of the flag as str
        """
        return self._prefix
    
    def __str__(self) -> str:
        return self.string_entity
    
    def __repr__(self) -> str:
        return f'Flag<name={self.name}, prefix={self.prefix}>'
        
    def __eq__(self, other: object) -> bool: 
        if isinstance(other, Flag):
            return self.string_entity == other.string_entity
        else:
            raise NotImplementedError


class InputFlag:
    def __init__(
        self, name: str, *,
        prefix: Literal['-', '--', '---'] = '--',
        value: str | None,
        status: ValidationStatus | None
    ):
        """
        Public. The entity of the flag of the entered command
        :param name: the name of the input flag
        :param prefix: the prefix of the input flag
        :param value: the value of the input flag
        :return: None
        """
        self._name = name
        self._prefix = prefix
        self._value = value
        self._status = status

    @property
    def value(self) -> str | None:
        """
        Public. Returns the value of the flag
        :return: the value of the flag as str
        """
        return self._value

    def set_value(self, value: str | None) -> None:
        """
        Private. Sets the value of the flag
        :param value: the flag value to set
        :return: None
        """
        self._value = value

    @property
    def name(self) -> str:
        """
        Public. Returns the name of the flag
        :return: the name of the flag as str
        """
        return self._name
    
    @property
    def prefix(self) -> str:
        """
        Public. Returns the prefix of the flag
        :return: the prefix of the flag as str
        """
        return self._prefix
    
    @property
    def status(self) -> ValidationStatus | None:
        """
        Public. Returns the status of the flag
        :return: the status of the flag as ValidationStatus
        """
        return self._status
    
    @property
    def string_entity(self) -> str:
        """
        Public. Returns a string representation of the flag
        :return: string representation of the flag as str
        """
        string_entity: str = self._prefix + self._name
        return string_entity

    def __str__(self) -> str:
        return f'{self.string_entity} {self.value}'
    
    def __repr__(self) -> str:
        return f'InputFlag<name={self.name}, prefix={self.prefix}, value={self.value}, status={self.status}>'

    def __eq__(self, other: object) -> bool: 
        if isinstance(other, InputFlag):
            return (
                self.name == other.name
                and self.value == other.value
            )
        else:
            raise NotImplementedError
    
    def set_status(self, status: ValidationStatus) -> None:
        """
        Private. Sets the status of the flag
        :param value: the flag status to set
        :return: None
        """
        self._status = status
