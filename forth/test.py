from lexer import lex
from vm import parse, eval
import sys

progFile = sys.argv[1]
lt = [progFile]
if len(sys.argv) > 2:
    args = sys.argv[2:]
    lt.extend(args)
# print(lt)


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

prog37 = """
get dup 0 >
{ 
    5 >=
    { "Greater than equal to 5" print { 10 { "." print } repeat } run }
    { "Less than 5" print
      "Enter \"yes\" to proceed and print numbers from 10 to 1 else \"no\"" put
      get dup "yes" s=
      {
        10 { dup 0 > } 
        { dup print dec } 
        while 
      }
      {
        "no" s=
        { "exited" print }
        { "invalid string entered" print }
        if
      }
      if
    }
    if
}
{ "Not positive" print }
if
"""

prog38 = """
0 { inc dup print } forever
"""

prog39 = """
{ print } [ 2 3 5 7 ] foreach
"""

prog40 = """
7 5 3 2 { + print } [ 2 3 5 7 ] foreach
"""

prog41 = """
false is-bool? print
"""

prog42 = """
argv len 1 > { argv 1 nth } { "y" } if
{ dup print } forever
"""

prog43 = """
{ dup 0 = { pop 1 } { dup dec fact * } if } 'fact def
5 fact print
"""

prog44 = """
{ x y + print } 'foo def
{ { 1 } 'x def { 2 } 'y def foo } 'bar def
bar
"""

prog45 = """
{ x x * print } 'square def
{ { dup } 'x def square } 'compute def
3 compute
"""

prog46 = """
[ 'apple 'banana 'cherry ] 1 nth is-symbol? print
[ 'apple 'banana 'cherry ] spread 'banana sym= print
"""

prog47 = """
{ 0 > { 'positive } { 'negative } if } 'sign def
3 sign put
-2 sign put
"""

prog48 = """
{ 1 } 'x def
{ x print } 'foo def
foo
{ 2 } 'x def 
foo
"""

prog49 = """
{ { 2 * put } [ 1 2 3 ] foreach } 'double def
double

"-------------------------------------" print

{ { 2 * } [ 1 2 3 ] foreach } 'double def
double put put put
"""

prog50 = """
1 { dup } 'fact def fact put put
"""

prog51 = """
'a 'hello put 'a dup is-symbol? pop sym= put
'hello is-symbol? put
"\"" put
"""

prog52 = """
{ dup 0 = { pop true } { dec odd } if } 'even def
{ dup 0 = { pop false } { dec even } if } 'odd def
5 even put
"""

prog53 = """
{
  dup 1 <=
  { pop 1 } 
  { dup dec fib rot dec dec fib + } 
  if 
} 'fib def
10 fib print
"""

# for t in lex(prog19):
#     print(t)
# eval(prog19)
# lexons = lex(prog)
# for i, t in enumerate(lexons):
#     print(f"{i}: {t}")

parsed = parse(prog, lt)
# print(parsed)
eval(parsed)