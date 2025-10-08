from abc import ABC


class BaseDividingLine(ABC):
    def __init__(self, unit_part: str = "-") -> None:
        """
        Private. The basic dividing line
        :param unit_part: the single part of the dividing line
        :return: None
        """
        self._unit_part: str = unit_part

    def get_unit_part(self) -> str:
        """
        Private. Returns the unit part of the dividing line
        :return: unit_part of dividing line as str
        """
        if len(self._unit_part) == 0:
            return " "
        else:
            return self._unit_part[0]


class StaticDividingLine(BaseDividingLine):
    def __init__(self, unit_part: str = "-", *, length: int = 25) -> None:
        """
        Public. The static dividing line
        :param unit_part: the single part of the dividing line
        :param length: the length of the dividing line
        :return: None
        """
        super().__init__(unit_part)
        self.length: int = length

    def get_full_static_line(self, *, is_override: bool) -> str:
        """
        Private. Returns the full line of the dividing line
        :param is_override: has the default text layout been redefined
        :return: full line of dividing line as str
        """
        if is_override:
            return f"\n{self.length * self.get_unit_part()}\n"
        else:
            return f"\n[dim]{self.length * self.get_unit_part()}[/dim]\n"


class DynamicDividingLine(BaseDividingLine):
    def __init__(self, unit_part: str = "-") -> None:
        """
        Public. The dynamic dividing line
        :param unit_part: the single part of the dividing line
        :return: None
        """
        super().__init__(unit_part)

    def get_full_dynamic_line(self, *, length: int, is_override: bool) -> str:
        """
        Private. Returns the full line of the dividing line
        :param length: the length of the dividing line
        :param is_override: has the default text layout been redefined
        :return: full line of dividing line as str
        """
        if is_override:
            return f"\n{length * self.get_unit_part()}\n"
        else:
            return f"\n[dim]{self.get_unit_part() * length}[/dim]\n"
