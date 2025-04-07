class BaseDividingLine:
    def __init__(self, unit_part: str = '-'):
        self.unit_part = unit_part

    def get_unit_part(self):
        if len(self.unit_part) == 0:
            return ' '
        else:
            return self.unit_part[0]

class StaticDividingLine(BaseDividingLine):
    def __init__(self, unit_part: str = '-', length: int = 25):
        super().__init__(unit_part)
        self.length = length

    def get_full_line(self):
        return f'\n[dim]{self.length * self.get_unit_part()}[/dim]\n'


class DynamicDividingLine(BaseDividingLine):
    def get_full_line(self, length: int):
        return f'\n[dim]{self.get_unit_part() * length}[/dim]\n'


