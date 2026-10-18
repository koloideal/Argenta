import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Measurement:
    name: str
    type_: str
    description: str
    seconds: float


@dataclass(frozen=True, slots=True)
class Side:
    python: str
    directory: str

    @classmethod
    def from_cli(cls, python: str, directory: str) -> "Side":
        # abspath, not resolve(): venv pythons are symlinks — resolving
        # them would escape the venv and lose the installed argenta
        return cls(os.path.abspath(python), os.path.abspath(directory))


@dataclass(frozen=True, slots=True)
class Comparison:
    type_: str
    description: str
    base: float
    head: float

    @property
    def ratio(self) -> float:
        return self.base / self.head
