a = BrokenPipeError()
def q(f):
    print(id(f))

print(id(a))
q(a)