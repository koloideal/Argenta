from argenta.command import Flag, PossibleValues

# Создание двух флагов с одинаковым именем и префиксом
flag1 = Flag(name="verbose", prefix="--")
flag2 = Flag(name="verbose", prefix="--")

# Сравнение флагов
print(flag1 == flag2)  # True

# Флаги с разными префиксами не равны
flag3 = Flag(name="verbose", prefix="-")
print(flag1 == flag3)  # False

# Флаги с разными именами не равны
flag4 = Flag(name="help", prefix="--")
print(flag1 == flag4)  # False

# Разные possible_values не влияют на равенство
flag5 = Flag(name="verbose", prefix="--", possible_values=PossibleValues.NEITHER)
flag6 = Flag(name="verbose", prefix="--", possible_values=["value1", "value2"])
print(flag5 == flag6)  # True (сравнение только по string_entity)
