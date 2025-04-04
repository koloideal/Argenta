from contextlib import redirect_stdout
import io


while True:
    with redirect_stdout(io.StringIO()) as f:
        a = input('rgsert')
        print(a)
        res = f.getvalue()
    print('-'*len(res))
    print(res.replace('\n', ''))
    print('-'*len(res))
