from argenta.command import Flag

verbose_flag = Flag(name="verbose", prefix="--")
short_flag = Flag(name="v", prefix="-")

# Отладочное представление
print(repr(verbose_flag))  # Flag<prefix=--, name=verbose>
print(repr(short_flag))  # Flag<prefix=-, name=v>

# В интерактивной консоли или отладчике
# >>> verbose_flag
# Flag<prefix=--, name=verbose>
