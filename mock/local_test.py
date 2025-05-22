from enum import Enum
from typing import Literal


class PossibleValues(Enum):
    DISABLE: Literal[False] = False
    ALL: Literal[True] = True

    def __eq__(self, other: bool) -> bool:
        return self.value == other


print(PossibleValues.DISABLE == False)
