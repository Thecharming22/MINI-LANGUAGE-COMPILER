import sys

if len(sys.argv) < 2:
    print("Usage: py main.py <file.genz>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "r") as f:
    code = f.read()

print("Source Code:\n")
print(code)
