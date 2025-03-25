from vm import eval
import sys

if len(sys.argv) != 2:
    print("Usage: ./run.sh <file>")
    sys.exit(1)

progFile = sys.argv[1]

with open(f"./{progFile}") as file:
    prog = file.read()

prog1 = """
"Hello, " get "!" concat concat put
"""

prog2 = """
2 3 + put
"""

prog3 = """
get get + put
"""

prog4 = """
10 2 / put
"""

prog5 = """
get get concat put
"""

prog6 = """
2 -3 - put
"""

prog7 = """
"Enter first number: " put get
"Enter second number: " put get
"Their sum is: " put + put
"""

eval(prog)