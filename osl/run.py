import argparse
from src.osl_eval import *
from pprint import pprint
import sys
from src.codegen import *
sys.setrecursionlimit(100000000)
from src.visualizer import *

def main():
    parser = argparse.ArgumentParser(description="osl Compiler/Interpreter")
    parser.add_argument(
        "--compile", "-c", 
        action="store_true", 
        help="Compile the code to bytecode"
    )
    parser.add_argument(
        "--run", "-i", 
        action="store_true", 
        help="Interpret and execute the code"
    )
    args = parser.parse_args()

    with open("code.osl") as f:
        code = f.read()

    parsed = parse(code)
    rcode = resolve(parsed)

    if args.compile:
        bb = bytearray(codegen(rcode))
        with open("bytecode.bin", "wb") as bytecode_file:
            bytecode_file.write(bb)
        result = parse_bytecode(bb)
        for opcode, operand in result:
           print(f"{opcode} {operand if operand is not None else ''}")
        print("Bytecode generated and saved to bytecode.bin")
        
    elif args.run:
        print(e(rcode))
        
    else:
        print("Please specify either --compile (-c) or --run (-i).")

if __name__ == "__main__":
    main()