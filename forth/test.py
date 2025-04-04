from lexer import lex
from vm import parse, eval
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

prog20 = """
1 [ 1 3 4 ] 3.34 4 false "true" list put
"""

prog21 = """
1 [ 1 3 4 ] 3.34 4 false "true" 3 listn dup put list put
"""

prog22 = """
1 [ 1 3 4 ] len dup put [ 1 2 ] 3.34 4 false "true" 3 listn dup put list put
"""

prog23 = """
{ "Hello" print }
"""

prog24 = """
{ "Hello" print } run
"""

prog25 = """
get 0 >
{ "Positive" print }
{ "Not positive" print }
if
"""

prog26 = """
10 { "." print } repeat
"""

prog27 = """
10 { dup 0 > } { dup print dec } while
"""

prog28 = """
1 { dup 5 <= } { dup print inc } while
"""

prog29 = """
"apple" "banana" lex< print
"""

prog30 = """
"hello" "hello" s= print
"""

prog30 = """
"world" "hello" s!= print
"""

prog31 = """
true false b!= print
"""

prog32 = """
true true b= print
"""

prog33 = """
"apple" "banana" lex<= print
"""

prog34 = """
"apple" "banana" lex>= print
"""

prog35 = """
"apple" "banana" lex> print
"""

prog36 = """
get dup 0 >
{ 
    > 5
    { "Greater than 5" print }
    { "Less than 5" print }
    if
}
{ "Not positive" print }
if
"""

# for t in lex(prog19):
#     print(t)
# eval(prog19)
# lexons = lex(prog)
# for i, t in enumerate(lexons):
#     print(f"{i}: {t}")

eval(parse(prog))