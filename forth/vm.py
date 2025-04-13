from lexer import *
from typing import List, Dict
class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        if not self.stack:
            print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nUnderflow!",end="")
            exit(1)
        return self.stack.pop()
    
    def peek(self):
        if not self.stack:
            print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nUnderflow!",end="")
            exit(1)
        return self.stack[-1]
    
    def __len__(self):
        return len(self.stack)
    
    def __repr__(self):
        return f"Stack({self.stack})"

@dataclass
class Object:
    pass
@dataclass
class NumberObj(Object):
    val: str

@dataclass
class BooleanObj(Object):
    val: str

@dataclass
class StringObj(Object):
    val: str

@dataclass
class SymbolObj(Object):
    val: str

@dataclass
class ListObject(Object):
    val: List[Object]
    
    def __len__(self):
        return len(self.val)
    
    def __getitem__(self, key):
        return self.val[key]
    
    def __repr__(self):
        return f"ListObject({self.val})"

@dataclass
class Token:
    pass
@dataclass
class ProgramObject(Object):
    val: List[Object]
    
    def __len__(self):
        return len(self.prog)
    
    def __getitem__(self, key):
        return self.val[key]
    
    def __repr__(self):
        return f"ProgramObject({self.val})"

def parse(s: str, args: List) -> List[Object]:
    tokens = lex(s)
    stack = Stack()
    
    for token in tokens:
        match token:
            case NumberToken(val):
                if '.' in val:
                    stack.push(NumberObj(float(val)))
                else:
                    stack.push(NumberObj(int(val)))
            
            case BooleanToken(val):
                stack.push(BooleanObj(val))
            
            case StringToken(val):
                stack.push(StringObj(val))
            
            case SymbolToken(val):
                stack.push(SymbolObj(val))
                            
            case WordToken(val):
                match val:
                    case "}":
                        l = []
                        while True:
                            if not stack:
                                print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nUnmatched {",end="")
                                exit(1)
                            x = stack.pop()
                            if isinstance(x, StringObj) and x.val == "{":
                                break
                            l.append(x)
                        stack.push(ProgramObject(l[::-1]))
                        
                    case "{":
                        stack.push(StringObj(val))
                    
                    case "argv":
                        l_ = []
                        for elt in args:
                            l_.append(StringObj(elt))
                        stack.push(ListObject(l_))
                    
                    case _:       
                        stack.push(WordToken(val))
                
            case OperatorToken(op):
                stack.push(OperatorToken(op))

    return stack.stack

def eval(objs: List, env: Dict = None, stack: Stack = None) -> None:
    if stack is None:
        stack = Stack()
        
    if env is None:
        env = {}
    
    i = 0
    while i < len(objs):
        obj = objs[i]
        i += 1
        match obj:
            case NumberObj(val):
                stack.push(NumberObj(val))
                
            case BooleanObj(val):
                stack.push(BooleanObj(val))
            
            case StringObj(val):
                stack.push(StringObj(val))
                            
            case ProgramObject(val):
                stack.push(ProgramObject(val))
            
            case ListObject(val):
                stack.push(ListObject(val))
            
            case SymbolObj(val):
                stack.push(SymbolObj(val))
                
            case WordToken(val):
                if val == "+":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val + b.val))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nAddition requires numbers",end="")
                        exit(1)

                elif val == "-":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val - b.val))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nSubtraction requires numbers",end="")
                        exit(1)
                    
                elif val == "*":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val * b.val))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nMultiplication requires numbers",end="")
                        exit(1)
                    
                elif val == "/":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val / b.val))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nDivision requires numbers",end="")
                        exit(1)
                    
                elif val == "^":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val ** b.val))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nExponentiation requires numbers",end="")
                        exit(1)
                
                elif val == ">":
                    b = stack.pop()
                    a = stack.pop()
                    # a and b have to numbers but push BooleanToken
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        if a.val > b.val:
                            stack.push(BooleanObj("true"))
                        else:
                            stack.push(BooleanObj("false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nGreater than requires numbers",end="")
                        exit(1)
                
                elif val == "<":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        if a.val < b.val:
                            stack.push(BooleanObj("true"))
                        else:
                            stack.push(BooleanObj("false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nLess than requires numbers",end="")
                        exit(1)
                
                elif val == ">=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        if a.val >= b.val:
                            stack.push(BooleanObj("true"))
                        else:
                            stack.push(BooleanObj("false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nGreater than or equal requires numbers",end="")
                        exit(1)
                
                elif val == "<=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        if a.val <= b.val:
                            stack.push(BooleanObj("true"))
                        else:
                            stack.push(BooleanObj("false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nLess than or equal requires numbers",end="")
                        exit(1)
                
                elif val == "=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        if a.val == b.val:
                            stack.push(BooleanObj("true"))
                        else:
                            stack.push(BooleanObj("false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nEquality requires numbers",end="")
                        exit(1)
                    
                elif val == "get":
                    s = input()
                    
                    # again do the lexer like check here!
                    f = None
                    j = 0
                    while j < len(s):
                        char = s[j]

                        if char == '"':
                            j, f = checkInputStr(j, s)
                            f = StringObj(f)
                        
                        elif char.isdigit() or (char == '-' and j + 1 < len(s) and s[j + 1].isdigit()):
                            j, f = checkInputNum(j, s)
                            f = NumberObj(f)
                        
                        # checking for BooleanToken same as Lexer
                        elif char.isalpha():
                            start = j
                            while j < len(s) and not s[j].isspace() and s[j] != '"':
                                j += 1
                            f = s[start:j]
                            if f in {"true", "false"}:
                                f = BooleanObj(f)
                            else:
                                print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nget says: Neither a number nor a string",end="")
                                exit(1)
                        
                        else:
                            print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nget says: Neither a number nor a string",end="")
                            exit(1)

                    if isinstance(f, NumberObj):
                        if '.' in f.val:
                            stack.push(NumberObj(float(f.val)))
                        else:
                            stack.push(NumberObj(int(f.val)))
                    else:
                        # BooleanObj
                        stack.push(f)
                    # print(f)
                        
                elif val == "put":
                    obj = stack.pop()
                    if isinstance(obj, NumberObj):
                        print(obj.val)
                    elif isinstance(obj, StringObj):
                        print('"' + obj.val + '"')
                    elif isinstance(obj, BooleanObj):
                        print(obj.val)
                    elif isinstance(obj, SymbolObj):
                        print(obj.val)
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nput requires a number, string or boolean",end="")
                        exit(1)
                    
                elif val == "pop":
                    stack.pop()
                    
                elif val == "dup":
                    x = stack.peek()
                    stack.push(x)
                    
                elif val == "rot":
                    if len(stack) < 2:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nrot requires at least 2 elements",end="")
                        exit(1)
                    x = stack.pop()
                    y = stack.pop()
                    stack.push(x)
                    stack.push(y)
                    
                elif val == "concat":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(StringObj(a.val + b.val))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nconcat requires two strings",end="")
                        exit(1)
                
                elif val == "]":
                    l = []
                    while True:
                        if not stack:
                            print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nUnmatched [",end="")
                            exit(1)
                        x = stack.pop()
                        if isinstance(x, StringObj) and x.val == "[":
                            break
                        l.append(x)
                    stack.push(ListObject(l[::-1]))
                
                elif val == "[":
                    stack.push(StringObj(val))
                
                elif val == "nth":
                    n = stack.pop()
                    l = stack.pop()
                    if not isinstance(n.val, int):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nnth requires an Integer",end="")
                        exit(1)
                    if not isinstance(l, ListObject):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nnth requires a List",end="")
                        exit(1)
                    if n.val < 0 or n.val >= len(l):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nIndex out of bounds",end="")
                        exit(1)
                    stack.push(l[n.val])
                
                elif val == "spread":
                    l = stack.pop()
                    if not isinstance(l, ListObject):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nspread requires a list",end="")
                        exit(1)
                    for item in l:
                        stack.push(item)

                elif val == "print":
                    print(stack.peek().val)
                
                elif val == "len":
                    l = stack.pop()
                    if isinstance(l, ListObject):
                        stack.push(NumberObj(len(l)))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nlen requires a List",end="")
                        exit(1)
                
                elif val == "listn":
                    n = stack.pop()
                    if not isinstance(n.val, int):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nlistn requires an Integer",end="")
                        exit(1)
                    
                    l = []
                    for _ in range(n.val):
                        l.append(stack.pop())
                        
                    stack.push(ListObject(l[::-1]))
                
                elif val == "list":
                    l = []
                    while stack:
                        l.append(stack.pop())
                    stack.push(ListObject(l[::-1]))
                           
                elif val == "run":
                    prog = stack.pop()
                    if isinstance(prog, ProgramObject):
                        eval(prog.val, env, stack)
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nrun requires a program",end="")
                        exit(1)
                    
                elif val == "if":
                    else_prog = stack.pop()
                    if_prog = stack.pop()
                    cond = stack.pop()
                    if not isinstance(if_prog, ProgramObject) or not isinstance(else_prog, ProgramObject):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nif requires a program",end="")
                        exit(1)
                    if isinstance(cond, BooleanObj):
                        if cond.val == "true":
                            eval(if_prog.val, env, stack)
                        else:
                            eval(else_prog.val, env, stack) 
                    
                elif val == "repeat":
                    procedure = stack.pop()
                    if not isinstance(procedure, ProgramObject):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nrepeat requires a program",end="")
                        exit(1)
                    n = stack.pop()
                    if not isinstance(n.val, int):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nrepeat requires an Integer",end="")
                        exit(1)
                    
                    if n.val < 0:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nrepeat requires a positive Integer",end="")
                        exit(1)
                    
                    for _ in range(n.val):
                        eval(procedure.val, env, stack)
                    
                elif val == "while":
                    procedure = stack.pop()
                    cond_procedure = stack.pop()
                    if not isinstance(procedure, ProgramObject) or not isinstance(cond_procedure, ProgramObject):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nwhile requires both the body and the condition to be a procedure",end="")
                        exit(1)
                    
                    # evaluate the condition
                    eval(cond_procedure.val, env, stack)
                    cond = stack.pop()
                    
                    if not isinstance(cond, BooleanObj):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nwhile condition must evaluate to a boolean",end="")
                        exit(1)
                    
                    while cond.val == "true":
                        eval(procedure.val, env, stack)
                        eval(cond_procedure.val, env, stack)
                        cond = stack.pop() 
                    
                elif val == "dec":
                    n = stack.pop()
                    if not isinstance(n, NumberObj):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\ndec requires a number",end="")
                        exit(1)
                    stack.push(NumberObj(n.val - 1))
                
                elif val == "inc":
                    n = stack.pop()
                    if not isinstance(n, NumberObj):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\ninc requires a number",end="")
                        exit(1)
                    stack.push(NumberObj(n.val + 1))
                 
                elif val == "forever":
                    procedure = stack.pop()
                    if not isinstance(procedure, ProgramObject):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nforever requires a program",end="")
                        exit(1)
                    
                    while True:
                        eval(procedure.val, env, stack)
                        
                elif val == "foreach":
                    l = stack.pop()
                    if not isinstance(l, ListObject):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nforeach requires a list",end="")
                        exit(1)
                    
                    procedure = stack.pop()
                    if not isinstance(procedure, ProgramObject):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nforeach requires a program",end="")
                        exit(1)
                    
                    for item in l:
                        stack.push(item)
                        eval(procedure.val, env, stack)
                
                elif val == "is-number?":
                    n = stack.pop()
                    if isinstance(n, NumberObj):
                        stack.push(BooleanObj("true"))
                    else:
                        stack.push(BooleanObj("false"))
                        
                elif val == "is-string?":
                    s = stack.pop()
                    if isinstance(s, StringObj):
                        stack.push(BooleanObj("true"))
                    else:
                        stack.push(BooleanObj("false"))
                        
                elif val == "is-bool?":
                    b = stack.pop()
                    if isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true"))
                    else:
                        stack.push(BooleanObj("false"))
                
                elif val == "is-list?":
                    l = stack.pop()
                    if isinstance(l, ListObject):
                        stack.push(BooleanObj("true"))
                    else:
                        stack.push(BooleanObj("false"))
                
                elif val == "is-symbol?":
                    s = stack.pop()
                    if isinstance(s, SymbolObj):
                        stack.push(BooleanObj("true"))
                    else:
                        stack.push(BooleanObj("false"))                               
                
                elif val == "def":
                    sym = stack.pop()
                    if not isinstance(sym, SymbolObj):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\ndef requires a symbol",end="")
                        exit(1)
                    prog = stack.pop()
                    if not isinstance(prog, ProgramObject):
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\ndef requires a program",end="")
                        exit(1)

                    word = sym.val[1:]
            
                    if word in {"true", "false", "and", "or", "not", "xor", "b=", "b!=", "s=", 
                                "s!=", "lex>", "lex<", "lex<=", "lex>=", "sym=", "get", "put", "pop",
                                "dup", "rot", "+", "-", "*", "/", "^", ">", "<", ">=", "<=", "=",
                                "argv", "if", "repeat", "while", "dec", "inc", "forever", "foreach",
                                "is-number?", "is-string?", "is-bool?", "is-list?", "is-symbol?",
                                "listn", "list", "nth", "spread", "concat", "print", "len",
                                "run", "def", "is-number?", "is-string?", "is-bool?", "is-list?",
                                "is-symbol?"}:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, f"\nSymbol {word} is a builtin identifier", end="")
                        exit(1)
                        
                    env[word] = prog
                
                else:
                    # print(env)
                    # print("="*100)
                    if val in env:
                        prog = env[val]
                        if isinstance(prog, ProgramObject):
                            eval(prog.val, env, stack)
                        else:
                            print("x" * 20, "RUNTIME ERROR", "x" * 20, f"\nSymbol {val} is not a program",end="")
                            exit(1)
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, f"\nUnknown word: {val}",end="")
                        exit(1)
      
            case OperatorToken(op):
                if op == "and":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val == "true" and b.val == "true" else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nand requires two booleans",end="")
                        exit(1)
                    
                elif op == "or":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val == "true" or b.val == "true" else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nor requires two booleans",end="")
                        exit(1)
                    
                elif op == "not":
                    a = stack.pop()
                    if isinstance(a, BooleanObj):
                        stack.push(BooleanObj("true" if a.val == "false" else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nnot requires a boolean",end="")
                        exit(1)
                
                elif op == "xor":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val != b.value else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nxor requires two booleans",end="")
                        exit(1)
                
                elif op == "b=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val == b.val else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nb= requires two booleans",end="")
                        exit(1)
                
                elif op == "b!=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val != b.val else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nb!= requires two booleans",end="")
                        exit(1)
                
                elif op == "s=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val == b.val else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\ns= requires two strings",end="")
                        exit(1)
                
                elif op == "s!=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val != b.val else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\ns!= requires two strings",end="")
                        exit(1)
                
                elif op == "lex<":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val < b.val else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nlex< requires two strings",end="")
                        exit(1)
                    
                elif op == "lex>":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val > b.val else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nlex> requires two strings",end="")
                        exit(1)
                
                elif op == "lex<=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val <= b.val else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nlex<= requires two strings",end="")
                        exit(1)
                
                elif op == "lex>=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val >= b.val else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nlex<= requires two strings",end="")
                        exit(1)
                
                elif op == "sym=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, SymbolObj) and isinstance(b, SymbolObj):
                        stack.push(BooleanObj("true" if a.val == b.val else "false"))
                    else:
                        print("x" * 20, "RUNTIME ERROR", "x" * 20, "\nsym= requires two symbols",end="")
                        exit(1)
                
                else:
                    print("x" * 20, "RUNTIME ERROR", "x" * 20, f"\nUnknown operator: {op}",end="")
                    exit(1)