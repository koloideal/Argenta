from argenta.command import Flag, PossibleValues

# Creating two flags with the same name and prefix
flag1 = Flag(name="verbose", prefix="--")
flag2 = Flag(name="verbose", prefix="--")

# Flag comparison
print(flag1 == flag2)  # True

# Flags with different prefixes are not equal
flag3 = Flag(name="verbose", prefix="-")
print(flag1 == flag3)  # False

# Flags with different names are not equal
flag4 = Flag(name="help", prefix="--")
print(flag1 == flag4)  # False

# Different possible_values do not affect equality
flag5 = Flag(name="verbose", prefix="--", possible_values=PossibleValues.NEITHER)
flag6 = Flag(name="verbose", prefix="--", possible_values=["value1", "value2"])
print(flag5 == flag6)
