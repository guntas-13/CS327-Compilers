from dataclasses import dataclass
from collections.abc import Iterator

@dataclass
class Token:
    pass

# 5 special tokens:
# :
# ,
# {
# }
# [
# ]

@dataclass
class SpecialToken(Token):
    sym: str

@dataclass
class StringToken(Token):
    val: str

@dataclass
class NumberToken(Token):
    val: str
    
@dataclass
class TrueToken(Token):
    pass

@dataclass
class FalseToken(Token):
    pass

@dataclass
class NullToken(Token):
    pass


def lex(s: str) -> Iterator[Token]:
    i = 0

    while i < len(s):
        char = s[i]

        if char.isspace():
            i += 1
            continue

        if char in {':', ',', '{', '}', '[', ']'}:
            yield SpecialToken(char)
            i += 1
            continue
        
        # comments as // are allowed
        if char == '/' and i + 1 < len(s) and s[i + 1] == '/':
            i += 2
            while i < len(s) and s[i] != '\n':
                i += 1
            continue
        
        if char == '"':
            i += 1
            start = i
            string = ""
            while i < len(s):
                char = s[i]
                if char == '"':
                    i += 1
                    yield StringToken(string)
                    break
                if char == '\\':
                    i += 1
                    if i >= len(s):
                        raise ValueError("Unterminated string")
                    escape_char = s[i]
                    if escape_char == '"':
                        string += '"'
                    elif escape_char == '\\':
                        string += '\\'
                    elif escape_char == '/':
                        string += '/'
                    elif escape_char == 'b':
                        string += '\b'
                    elif escape_char == 'f':
                        string += '\f'
                    elif escape_char == 'n':
                        string += '\n'
                    elif escape_char == 'r':
                        string += '\r'
                    elif escape_char == 't':
                        string += '\t'
                    elif escape_char == 'u':
                        if i + 4 >= len(s):
                            raise ValueError("Unterminated unicode escape sequence")
                        hex_value = s[i+1:i+5]
                        if all(c in '0123456789abcdefABCDEF' for c in hex_value):
                            string += chr(int(hex_value, 16))
                            i += 4
                        else:
                            raise ValueError(f"Invalid unicode escape sequence at index {i}: \\u{hex_value}")
                    else:
                        raise ValueError(f"Invalid escape character at index {i}: \\{escape_char}")
                else:
                    string += char
                i += 1
            else:
                raise ValueError("Unterminated string")
            continue

        if char.isdigit() or (char == '-' and i + 1 < len(s) and s[i + 1].isdigit()):
            start = i
            i += 1
            while i < len(s) and (s[i].isdigit() or s[i] in '.eE+_-'):
                # underscores as number separators are allowed
                if s[i] == '_':
                    if i + 1 < len(s) and s[i + 1].isdigit():
                        i += 1
                        continue
                    else:
                        raise ValueError("Number cannot have consecutive underscores or end with an underscore")
                i += 1
            num_str = s[start:i]
            yield NumberToken(num_str)
            continue

        if s.startswith('true', i):
            yield TrueToken()
            i += 4
            continue

        if s.startswith('false', i):
            yield FalseToken()
            i += 5
            continue

        if s.startswith('null', i):
            yield NullToken()
            i += 4
            continue

        raise ValueError(f"Unexpected character at index {i}: {char}")