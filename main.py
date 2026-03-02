import sys
from lexer import Lexer

if len(sys.argv) < 2:
    print("Usage: py main.py <file.genz>")
    sys.exit(1)

filename = sys.argv[1]
file = open(filename, "r")
code = file.read()
lex = Lexer(code)
tokens = lex.tokenize()
print(tokens)
