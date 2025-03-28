from lexer import *
from typing import List

class ListObject:
    def __init__(self, items: List):
        self.items = items

    def __repr__(self):
        return f"ListObject({self.items})"

    def __getitem__(self, index):
        return self.items[index]
    
    def __len__(self):
        return len(self.items)
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
    
    
def eval(s: str, stack: Stack = None):
    if stack is None:
        stack = Stack()
        
    tokens = lex(s)
    
    for token in tokens:
        match token:
            case NumberToken(val):
                if '.' in val:
                    stack.push(float(val))
                else:
                    stack.push(int(val))
            
            case BooleanToken(val):
                stack.push(BooleanToken(val))
            
            case StringToken(val):
                stack.push(val)
                                 
            case WordToken(val):
                if val == "+":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        stack.push(a + b)
                    else:
                        raise ValueError("Addition requires numbers")

                elif val == "-":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        stack.push(a - b)
                    else:
                        raise ValueError("Subtraction requires numbers")
                    
                elif val == "*":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        stack.push(a * b)
                    else:
                        raise ValueError("Multiplication requires numbers")
                    
                elif val == "/":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        stack.push(a / b)
                    else:
                        raise ValueError("Division requires numbers")
                    
                elif val == "^":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        stack.push(a ** b)
                    else:
                        raise ValueError("Exponentiation requires numbers")
                
                elif val == ">":
                    b = stack.pop()
                    a = stack.pop()
                    # a and b have to numbers but push BooleanToken
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        if a > b:
                            stack.push(BooleanToken("true"))
                        else:
                            stack.push(BooleanToken("false"))
                    else:
                        raise ValueError("Greater than requires numbers")
                
                elif val == "<":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        if a < b:
                            stack.push(BooleanToken("true"))
                        else:
                            stack.push(BooleanToken("false"))
                    else:
                        raise ValueError("Less than requires numbers")
                
                elif val == ">=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        if a >= b:
                            stack.push(BooleanToken("true"))
                        else:
                            stack.push(BooleanToken("false"))
                    else:
                        raise ValueError("Greater than or equal requires numbers")
                
                elif val == "<=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        if a <= b:
                            stack.push(BooleanToken("true"))
                        else:
                            stack.push(BooleanToken("false"))
                    else:
                        raise ValueError("Less than or equal requires numbers")
                
                elif val == "=":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        if a == b:
                            stack.push(BooleanToken("true"))
                        else:
                            stack.push(BooleanToken("false"))
                    else:
                        raise ValueError("Equality requires numbers")
                    
                elif val == "get":
                    s = input()
                    
                    # again do the lexer like check here!
                    f = None
                    i = 0
                    while i < len(s):
                        char = s[i]

                        if char == '"':
                            i, f = checkInputStr(i, s)
                            f = StringToken(f)
                        
                        elif char.isdigit() or (char == '-' and i + 1 < len(s) and s[i + 1].isdigit()):
                            i, f = checkInputNum(i, s)
                            f = NumberToken(f)
                        
                        # checking for BooleanToken same as Lexer
                        elif char.isalpha():
                            start = i
                            while i < len(s) and not s[i].isspace() and s[i] != '"':
                                i += 1
                            f = s[start:i]
                            if f in {"true", "false"}:
                                f = BooleanToken(f)
                            else:
                                raise ValueError("get says: Neither a number nor a string")
                        
                        else:
                            raise ValueError("get says: Neither a number nor a string")

                    if isinstance(f, NumberToken):
                        if '.' in f.val:
                            stack.push(float(f.val))
                        else:
                            stack.push(int(f.val))
                    elif isinstance(f, StringToken):
                        stack.push(f.val)
                    else:
                        # BooleanToken
                        stack.push(f)
                        
                elif val == "put":
                    value = stack.pop()
                    if isinstance(value, BooleanToken):
                        print(value.value)
                    else:
                        print(value)
                    
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
                    if isinstance(a, str) and isinstance(b, str):
                        stack.push(a + b)
                    else:
                        raise ValueError("concat requires two strings")
                
                elif val == "]":
                    l = []
                    while True:
                        if not stack:
                            raise ValueError("Unmatched [")
                        x = stack.pop()
                        if isinstance(x, str) and x == "[":
                            break
                        l.append(x)
                    stack.push(ListObject(l[::-1]))
                
                elif val == "[":
                    stack.push("[")
                
                elif val == "nth":
                    n = stack.pop()
                    l = stack.pop()
                    if not isinstance(n, int):
                        raise ValueError("nth requires an integer")
                    if not isinstance(l, ListObject):
                        raise ValueError("nth requires a list")
                    if n < 0 or n >= len(l):
                        raise ValueError("Index out of bounds")
                    stack.push(l[n])
                
                elif val == "spread":
                    l = stack.pop()
                    if not isinstance(l, ListObject):
                        raise ValueError("spread requires a list")
                    for item in l:
                        stack.push(item)
                
                else:
                    raise ValueError(f"Unknown word: {val}")
                
            case BooleanOperatorToken(op):
                if op == "and":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanToken) and isinstance(b, BooleanToken):
                        stack.push(BooleanToken("true" if a.value == "true" and b.value == "true" else "false"))
                    else:
                        raise ValueError("and requires two booleans")
                    
                elif op == "or":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanToken) and isinstance(b, BooleanToken):
                        stack.push(BooleanToken("true" if a.value == "true" or b.value == "true" else "false"))
                    else:
                        raise ValueError("or requires two booleans")
                    
                elif op == "not":
                    a = stack.pop()
                    if isinstance(a, BooleanToken):
                        stack.push(BooleanToken("true" if a.value == "false" else "false"))
                    else:
                        raise ValueError("not requires a boolean")
                
                elif op == "xor":
                    b = stack.pop()
                    a = stack.pop()
                    if isinstance(a, BooleanToken) and isinstance(b, BooleanToken):
                        stack.push(BooleanToken("true" if a.value != b.value else "false"))
                    else:
                        raise ValueError("xor requires two booleans")
                else:
                    raise ValueError(f"Unknown boolean operator: {op}")