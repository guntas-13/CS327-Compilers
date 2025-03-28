from lexer import lex
from vm import eval
import sys

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

prog8 = """
true false and put
"""

prog9 = """
get get or put
"""

prog10 = """
45 44 > 45 45 < or put
"""

prog11 = """
[ 1 2 3 4 5 6 pop pop pop ]
"""

prog12 = """
[ 1 2 [ 3 4 ] ]
"""

prog13 = """
[ pop ]
"""

prog14 = """
[ 1 2 3 ] 2 nth put
"""

prog15 = """
[ 1 2 [ 3 4 ] ] 2 nth 0 nth put
"""

prog16 = """
[ 1 2 3 ] spread * + put
"""

prog17 = """
[ [ 1 2 3 ] ] spread spread put put put
"""

prog18 = """
[ [ get get get ] ] dup put spread put
"""

prog19 = """
[ "guntas" true 1 get ] spread put put put put
"""

# for t in lex(prog19):
#     print(t)
# eval(prog19)

eval(prog)