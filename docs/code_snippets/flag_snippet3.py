from argenta.command import Flag

# Создание флагов с разными префиксами
verbose_flag = Flag(name="verbose", prefix="--")
short_flag = Flag(name="v", prefix="-")
triple_flag = Flag(name="debug", prefix="---")

# Получение строкового представления
print(verbose_flag.string_entity)  # --verbose
print(short_flag.string_entity)    # -v
print(triple_flag.string_entity)   # ---debug
