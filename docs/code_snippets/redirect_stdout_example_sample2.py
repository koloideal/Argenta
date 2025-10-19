from argenta.app import App
from argenta.app.dividing_line import StaticDividingLine

# Все роутеры по умолчанию будут использовать статическую линию длиной 50 символов
# (если для них не отключен перехват stdout)
app = App(dividing_line=StaticDividingLine(length=50))