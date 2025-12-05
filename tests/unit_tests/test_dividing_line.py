from argenta.app.dividing_line import DynamicDividingLine, StaticDividingLine


def test_get_static_dividing_line_full_line():
    line = StaticDividingLine('-')
    assert line.get_full_static_line(is_override=True).count('-') == 25
    
def test_get_static_dividing_line2_full_line():
    line = StaticDividingLine('-', length=5)
    assert line.get_full_static_line(is_override=False) == '\n[dim]-----[/dim]\n'
    
def test_get_dividing_line_unit_part():
    line = StaticDividingLine('')
    assert line.get_unit_part() == ' '

def test_get_dividing_line2_unit_part():
    line = StaticDividingLine('+-0987654321!@#$%^&*()_')
    assert line.get_unit_part() == '+'

def test_get_dynamic_dividing_line_full_line():
    line = DynamicDividingLine()
    assert line.get_full_dynamic_line(length=20, is_override=True).count('-') == 20
    
def test_get_dynamic_dividing_line2_full_line():
    line = DynamicDividingLine()
    assert line.get_full_dynamic_line(length=5, is_override=False) == '\n[dim]-----[/dim]\n'
    
def test_get_dynamic_dividing_line_unit_part():
    line = DynamicDividingLine('')
    assert line.get_unit_part() == ' '

def test_get_dynamic_dividing_line2_unit_part():
    line = DynamicDividingLine('45n352834528&^%@&*T$G')
    assert line.get_unit_part() == '4'


