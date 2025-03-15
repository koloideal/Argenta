import re


def test(string):
    return bool(re.match(r'\ntest command\n(.|\s)*\nsome command\n', string))

print(test('test command tpgm4tigm4tigmt\n i0hhmi6h some command'))
