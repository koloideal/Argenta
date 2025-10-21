from argenta import App
from argenta.app import StaticDividingLine, DynamicDividingLine

# Создание статической линии из символов "=" длиной 40
static_line = StaticDividingLine(unit_part="=", length=40)

# Создание динамической линии из символов "*"
dynamic_line = DynamicDividingLine(unit_part="*")

# Приложение со статической линией
app_with_static_line = App(dividing_line=static_line)

# Приложение с динамической линией (поведение по умолчанию, но с кастомным символом)
app_with_dynamic_line = App(dividing_line=dynamic_line)