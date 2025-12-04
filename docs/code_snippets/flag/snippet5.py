from argenta.command import Flag

verbose_flag = Flag(name="verbose", prefix="--")
short_flag = Flag(name="v", prefix="-")

# Debug view
print(repr(verbose_flag))  # Flag<prefix=--, name=verbose>
print(repr(short_flag))  # Flag<prefix=-, name=v>

# In an interactive console or debugger
# >>> verbose_flag
# Flag<prefix=--, name=verbose>
