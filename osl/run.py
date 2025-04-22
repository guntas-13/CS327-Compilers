from osl_eval import *
from pprint import pprint
import sys
from codegen import *
sys.setrecursionlimit(100000000)
from visualizer import *

with open("q8_22110089.osl") as f:
    code = f.read()
    
# print(code)
# print()

# for i, t in enumerate(lex(code)):
#     print(f"{i}: {t}")
# print()
parsed = parse(code)
# pprint(parsed)
rcode = resolve(parsed)
# pprint(rcode)
# print()
print(e(rcode))
# print(codegen(rcode))
# bb = bytearray(codegen(rcode))
# # print(bb)
# with open("bytecode.bin", "wb") as bytecode_file:
#     bytecode_file.write(bb)

# result = parse_bytecode(bb)
# for opcode, operand in result:
#    print(f"{opcode} {operand if operand is not None else ''}")