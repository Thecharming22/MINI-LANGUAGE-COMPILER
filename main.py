import sys
from lexer import Lexer

def run_lexer(code):
    lex = Lexer(code)
    tokens = lex.tokenize()
    return tokens

if len(sys.argv) < 2:
    print("Usage: py main.py <file.genz>")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename, "r") as file:
        code = file.read()

    tokens = run_lexer(code)
    print("\n--- TOKENS ---")
    for t in tokens:
        print(t)

except FileNotFoundError:
    print("File not found!")