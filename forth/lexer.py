from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Token:
    pass
@dataclass
class StringToken(Token):
    val: str
@dataclass
class NumberToken(Token):
    val: str
@dataclass
class BooleanToken(Token):
    value: str
@dataclass
class WordToken(Token):
    val: str
@dataclass
class OperatorToken(Token):
    op: str
@dataclass
class SymbolToken(Token):
    sym: str

def checkInputStr(i:int, s: str) -> Tuple[int, str]:
    i += 1
    string = ""
    while i < len(s):
        char = s[i]
        if char == '"':
            if i + 1 == len(s) or s[i + 1].isspace():
                i += 1
                return i, string
            else:
                print("x" * 20, "COMPILE TIME ERROR", "x" * 20, "\nInvalid character after string", end="")
                exit(1)

        if char == '\\':
            i += 1
            if i >= len(s):
                print("x" * 20, "COMPILE TIME ERROR", "x" * 20, "\nUnterminated string", end="")
                exit(1)
            escape_char = s[i]
            if escape_char == '"':
                string += '"'
            elif escape_char == '\\':
                string += '\\'
                string += '\f'
            elif escape_char == 'n':
                string += '\n'
            elif escape_char == 't':
                string += '\t'
            else:
                print("x" * 20, "COMPILE TIME ERROR", "x" * 20, f"\nInvalid escape character at index {i}: \\{escape_char}")
                exit(1)
        else:
            string += char
        i += 1
    else:
        print("x" * 20, "COMPILE TIME ERROR", "x" * 20, "\nUnterminated string", end="")
        exit(1)

def checkInputNum(i:int, s: str) -> Tuple[int, str]:
    start = i
    i += 1
    while i < len(s) and (s[i].isdigit() or s[i] == '.'):
        i += 1
    num_str = s[start:i]
    return i, num_str

def lex(s: str) -> List[Token]:
    i = 0
    tokens = []
    
    while i < len(s):
        char = s[i]
        
        if char.isspace():
            i += 1
            continue
        
        if char == '"':
            i, string = checkInputStr(i, s)
            tokens.append(StringToken(string))
        
        # symbols are like words but start with a single quote '
        elif char == "'":
            if i >= len(s):
                print("x" * 20, "COMPILE TIME ERROR", "x" * 20, "\nUnterminated symbol", end="")
                exit(1)
            start = i
            i += 1
            while i < len(s):
                if (s[i].isalnum() or s[i] == '_' or s[i] == '-'):
                    i += 1
                elif s[i].isspace():
                    break
                else:
                    print("x" * 20, "COMPILE TIME ERROR", "x" * 20, f"\nInvalid symbol character '{s[i]}' at position {i}")
                    exit(1)
            word = s[start:i]
            if not word or not word[1].isalpha() or not word[1] != '_':
                print("x" * 20, "COMPILE TIME ERROR", "x" * 20, f"\nInvalid symbol '{word}' at position {start}")
                exit(1)
            tokens.append(SymbolToken(word))
        
        elif char.isdigit() or (char == '-' and i + 1 < len(s) and s[i + 1].isdigit()):
            i, num_str = checkInputNum(i, s)
            tokens.append(NumberToken(num_str))
        
        elif s[i].isalpha() or s[i] in {'+', '-', '*', '/', '^', "<", ">", "=", '!', '[', ']', '{', '}', '?'}:
            start = i
            while i < len(s) and not s[i].isspace() and s[i] != '"':
                i += 1
            word = s[start:i]
            
            if word in {"true", "false"}:
                tokens.append(BooleanToken(word))
            elif word in {"and", "or", "not", "xor", "b=", "b!=", "s=", "s!=", "lex>", "lex<", "lex<=", "lex>=", "sym="}:
                tokens.append(OperatorToken(word))
            else:
                if word[0].isdigit():
                    print("x" * 20, "COMPILE TIME ERROR", "x" * 20, f"\nInvalid word '{word}' at position {start}")
                    exit(1)
                else:
                    tokens.append(WordToken(word))

        else:
            print("x" * 20, "COMPILE TIME ERROR", "x" * 20, f"\nUnexpected character '{s[i]}' at position {i}")
            exit(1)
    
    return tokens