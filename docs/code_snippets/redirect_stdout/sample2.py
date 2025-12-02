from argenta import App
from argenta.app import StaticDividingLine

# All routers will use static line with length 50 by default
app = App(dividing_line=StaticDividingLine(length=50))
