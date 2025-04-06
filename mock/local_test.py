from contextlib import redirect_stdout
import io
import string


while True:
    with redirect_stdout(io.StringIO()) as f:
        a = input()
        print(a)
        res = f.getvalue()
    res = ''.join([x for x in res if x in string.printable])
    print('-'*len(res))
    print(res.strip('\n'))
    print('-'*len(res))
