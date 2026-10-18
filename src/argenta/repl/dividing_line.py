import re

_ANSI_ESCAPE_RE = re.compile(r"\u001b\[[0-9;]*m")


class BaseDividingLine:
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

    def line(self) -> str:
        """
        Private. Returns the raw dividing line of the configured length
        :return: dividing line as str
        """
        return self.length * self.get_unit_part()


class DynamicDividingLine(BaseDividingLine):
    def __init__(
        self, unit_part: str = "-", *, min_length: int = 10, max_length: int = 100
    ) -> None:
        """
        Public. The dynamic dividing line, sized to the longest output line
        :param unit_part: the single part of the dividing line
        :param min_length: the shortest line drawn for short output
        :param max_length: the longest line drawn for wide output
        :return: None
        """
        super().__init__(unit_part)
        self.min_length: int = min_length
        self.max_length: int = max_length

    def line_for(self, framed_text: str) -> str:
        """
        Private. Returns the raw dividing line matching the longest line
        of the content, ANSI escapes ignored, clamped to the length bounds
        :param framed_text: the framed output
        :return: dividing line as str
        """
        clear_text = _ANSI_ESCAPE_RE.sub("", framed_text)
        longest = max(len(text_line) for text_line in clear_text.split("\n"))
        length = min(max(longest, self.min_length), self.max_length)
        return length * self.get_unit_part()
