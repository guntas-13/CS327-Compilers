import sys
from parser import *

# s = open('input4.json', "r").read()

# for t in lex(s):
#     print(t)

# print() 
# top = parse(s)
# pprint(top)  
# print()
# print(type(top.a))
# print(top.b[top.a])
# exit()

if len(sys.argv) != 3:
    print("Usage: ./run.sh <query> <filename>")
    sys.exit(1)

jsonFile = sys.argv[1]
q = sys.argv[2]

top = parse(open(jsonFile, "r").read())
print(eval(q))