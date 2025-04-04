from lexer import *
from typing import List
class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        if not self.stack:
            raise IndexError("Underflow!")
        return self.stack.pop()
    
    def peek(self):
        if not self.stack:
            raise IndexError("Underflow!")
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

def parse(s: str) -> List[Object]:
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
                            
            case WordToken(val):
                match val:
                    case "}":
                        l = []
                        while True:
                            if not stack:
                                raise ValueError("Unmatched {")
                            x = stack.pop()
                            if isinstance(x, StringObj) and x.val == "{":
                                break
                            l.append(x)
                        stack.push(ProgramObject(l[::-1]))
                        
                    case "{":
                        stack.push(StringObj(val))
                    
                    case _:       
                        stack.push(WordToken(val))
                
            case BooleanOperatorToken(op):
                stack.push(BooleanOperatorToken(op))
                
            case StringOperatorToken(op):
                stack.push(StringOperatorToken(op))
    
    return stack.stack

def eval(objs: List, stack: Stack = None):
    if stack is None:
        stack = Stack()
    
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
                
            case WordToken(val):
                if val == "+":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val + b.val))
                    else:
                        raise ValueError("Addition requires numbers")

                elif val == "-":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val - b.val))
                    else:
                        raise ValueError("Subtraction requires numbers")
                    
                elif val == "*":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val * b.val))
                    else:
                        raise ValueError("Multiplication requires numbers")
                    
                elif val == "/":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val / b.val))
                    else:
                        raise ValueError("Division requires numbers")
                    
                elif val == "^":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        stack.push(NumberObj(a.val ** b.val))
                    else:
                        raise ValueError("Exponentiation requires numbers")
                
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
                        raise ValueError("Greater than requires numbers")
                
                elif val == "<":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        if a.val < b.val:
                            stack.push(BooleanObj("true"))
                        else:
                            stack.push(BooleanObj("false"))
                    else:
                        raise ValueError("Less than requires numbers")
                
                elif val == ">=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        if a.val >= b.val:
                            stack.push(BooleanObj("true"))
                        else:
                            stack.push(BooleanObj("false"))
                    else:
                        raise ValueError("Greater than or equal requires numbers")
                
                elif val == "<=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        if a.val <= b.val:
                            stack.push(BooleanObj("true"))
                        else:
                            stack.push(BooleanObj("false"))
                    else:
                        raise ValueError("Less than or equal requires numbers")
                
                elif val == "=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, NumberObj) and isinstance(b, NumberObj):
                        if a.val == b.val:
                            stack.push(BooleanObj("true"))
                        else:
                            stack.push(BooleanObj("false"))
                    else:
                        raise ValueError("Equality requires numbers")
                    
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
                                raise ValueError("get says: Neither a number nor a string")
                        
                        else:
                            raise ValueError("get says: Neither a number nor a string")

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
                    else:
                        raise ValueError("put requires a number, string or boolean")
                    
                elif val == "pop":
                    stack.pop()
                    
                elif val == "dup":
                    x = stack.peek()
                    stack.push(x)
                    
                elif val == "rot":
                    if len(stack) < 2:
                        raise ValueError("rot requires at least 2 elements")
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
                        raise ValueError("concat requires two strings")
                
                elif val == "]":
                    l = []
                    while True:
                        if not stack:
                            raise ValueError("Unmatched [")
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
                        raise ValueError("nth requires an Integer")
                    if not isinstance(l, ListObject):
                        raise ValueError("nth requires a List")
                    if n.val < 0 or n.val >= len(l):
                        raise ValueError("Index out of bounds")
                    stack.push(l[n.val])
                
                elif val == "spread":
                    l = stack.pop()
                    if not isinstance(l, ListObject):
                        raise ValueError("spread requires a list")
                    for item in l:
                        stack.push(item)

                elif val == "print":
                    print(stack.peek().val)
                
                elif val == "len":
                    l = stack.pop()
                    if isinstance(l, ListObject):
                        stack.push(NumberObj(len(l)))
                    else:
                        raise ValueError("len requires a List")
                
                elif val == "listn":
                    n = stack.pop()
                    if not isinstance(n.val, int):
                        raise ValueError("listn requires an Integer")
                    
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
                        eval(prog.val, stack)
                    else:
                        raise ValueError("run requires a program")
                    
                elif val == "if":
                    else_prog = stack.pop()
                    if_prog = stack.pop()
                    cond = stack.pop()
                    if not isinstance(if_prog, ProgramObject) or not isinstance(else_prog, ProgramObject):
                        raise ValueError("if requires a program")
                    if isinstance(cond, BooleanObj):
                        if cond.val == "true":
                            eval(if_prog.val, stack)
                        else:
                            eval(else_prog.val, stack) 
                    
                elif val == "repeat":
                    procedure = stack.pop()
                    if not isinstance(procedure, ProgramObject):
                        raise ValueError("repeat requires a program")
                    n = stack.pop()
                    if not isinstance(n.val, int):
                        raise ValueError("repeat requires an Integer")
                    
                    if n.val < 0:
                        raise ValueError("repeat requires a positive Integer")
                    
                    for _ in range(n.val):
                        eval(procedure.val, stack)
                    
                elif val == "while":
                    procedure = stack.pop()
                    cond_procedure = stack.pop()
                    if not isinstance(procedure, ProgramObject) or not isinstance(cond_procedure, ProgramObject):
                        raise ValueError("while requires both the body and the condition to be a procedure")
                    
                    # evaluate the condition
                    eval(cond_procedure.val, stack)
                    cond = stack.pop()
                    
                    if not isinstance(cond, BooleanObj):
                        raise ValueError("while condition must evaluate to a boolean")
                    
                    while cond.val == "true":
                        eval(procedure.val, stack)
                        eval(cond_procedure.val, stack)
                        cond = stack.pop() 
                    
                elif val == "dec":
                    n = stack.pop()
                    if not isinstance(n, NumberObj):
                        raise ValueError("dec requires a number")
                    stack.push(NumberObj(n.val - 1))
                
                elif val == "inc":
                    n = stack.pop()
                    if not isinstance(n, NumberObj):
                        raise ValueError("inc requires a number")
                    stack.push(NumberObj(n.val + 1))
                                    
                else:
                    raise ValueError(f"Unknown word: {val}")
                  
            case BooleanOperatorToken(op):
                if op == "and":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val == "true" and b.val == "true" else "false"))
                    else:
                        raise ValueError("and requires two booleans")
                    
                elif op == "or":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val == "true" or b.val == "true" else "false"))
                    else:
                        raise ValueError("or requires two booleans")
                    
                elif op == "not":
                    a = stack.pop()
                    if isinstance(a, BooleanObj):
                        stack.push(BooleanObj("true" if a.val == "false" else "false"))
                    else:
                        raise ValueError("not requires a boolean")
                
                elif op == "xor":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val != b.value else "false"))
                    else:
                        raise ValueError("xor requires two booleans")
                
                elif op == "b=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val == b.val else "false"))
                    else:
                        raise ValueError("b= requires two booleans")
                
                elif op == "b!=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanObj) and isinstance(b, BooleanObj):
                        stack.push(BooleanObj("true" if a.val != b.val else "false"))
                    else:
                        raise ValueError("b!= requires two booleans")
                
                else:
                    raise ValueError(f"Unknown boolean operator: {op}")
            
            case StringOperatorToken(op):
                if op == "s=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val == b.val else "false"))
                    else:
                        raise ValueError("s= requires two strings")
                
                elif op == "s!=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val != b.val else "false"))
                    else:
                        raise ValueError("s!= requires two strings")
                
                elif op == "lex<":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val < b.val else "false"))
                    else:
                        raise ValueError("lex< requires two strings")
                    
                elif op == "lex>":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val > b.val else "false"))
                    else:
                        raise ValueError("lex> requires two strings")
                
                elif op == "lex<=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val <= b.val else "false"))
                    else:
                        raise ValueError("lex<= requires two strings")
                
                elif op == "lex>=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, StringObj) and isinstance(b, StringObj):
                        stack.push(BooleanObj("true" if a.val >= b.val else "false"))
                    else:
                        raise ValueError("lex<= requires two strings")

                else:
                    raise ValueError(f"Unknown string operator: {op}")