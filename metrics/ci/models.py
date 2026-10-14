from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Measurement:
    name: str
    type_: str
    description: str
    seconds: float


@dataclass(frozen=True, slots=True)
class Comparison:
    type_: str
    description: str
    base: float
    head: float

    @property
    def ratio(self) -> float:
        return self.base / self.head
