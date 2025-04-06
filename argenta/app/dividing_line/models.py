from collections.abc import Sized


def check(string: str):
    if len(string) != 1:
        raise ValueError


class BaseDividingLine:
    def __init__(self, unit_part: check):
        self.unit_part = unit_part


BaseDividingLine('sygu')

