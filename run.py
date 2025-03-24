from calculator_extended_resolved import e, resolve, parse, lex
from pprint import pprint

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