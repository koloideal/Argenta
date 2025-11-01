from argenta.command import Flag, Flags

flags = Flags([
    Flag("first"),
    Flag("second"),
    Flag("third")
])

print(flags[0].name)
# first

print(flags[1].name)
# second

print(flags[2].name)
# third