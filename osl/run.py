from osl_eval import *
from pprint import pprint
import sys
sys.setrecursionlimit(100000000)

with open("code.txt") as f:
    code = f.read()
    
print(code)
print()

for i, t in enumerate(lex(code)):
    print(f"{i}: {t}")
print()
rcode = resolve(parse(code))
pprint(rcode)
print()
print(e(rcode))