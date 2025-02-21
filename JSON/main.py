import sys
from parser import *
from pprint import pprint

# s = open('Lab.txt', "r").read()

# for t in lex(s):
#     print(t)

# print() 
# top = parse(s)
# pprint(top)  
# print()
# print(top.x)
# print(top.h)
# print(top.a)
# print(top.i[top.g[0] - 1])
# # print(top.b[2])
# # print(type(top.a))
# # print(top.b[top.a])
# # print(top.b[top.a].c[top.a])
# # print(type(top.b[top.a].c[top.a]))
# exit()

if len(sys.argv) != 3:
    print("Usage: ./run.sh <query> <filename>")
    sys.exit(1)

jsonFile = sys.argv[2]
q = sys.argv[1]

top = parse(open(jsonFile, "r").read())
print(eval(q))