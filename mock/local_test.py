import argparse

parser = argparse.ArgumentParser(prog='myprogram')
_ = parser.add_argument('--foo', help='foo of the %(prog)s program')
print(vars(parser.parse_args()))