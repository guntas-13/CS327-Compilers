from lexer import *

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
                    
                elif val == "get":
                    s = input()
                    
                    # again do the lexer like check here!
                    f = None
                    i = 0
                    while i < len(s):
                        char = s[i]

                        if char == '"':
                            i, f = checkInputStr(i, s)
                        
                        elif char.isdigit() or (char == '-' and i + 1 < len(s) and s[i + 1].isdigit()):
                            i, f = checkInputNum(i, s)
                        
                        else:
                            raise ValueError("get says: Neither a number nor a string")

                    try:
                        if '.' in f:
                            stack.push(float(f))
                        else:
                            stack.push(int(f))
                    except ValueError:
                        stack.push(f)  # Push as string if not a number
                        
                elif val == "put":
                    value = stack.pop()
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
                else:
                    raise ValueError(f"Unknown word: {val}")