from argenta import App
from argenta.app import StaticDividingLine

# Все роутеры по умолчанию будут использовать статическую линию длиной 50 символов
app = App(dividing_line=StaticDividingLine(length=50))
