from typing import cast, Literal

print(cast(Literal['-', '--', '---'], '----'))