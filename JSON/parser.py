from more_itertools import peekable
from typing import List, Dict, Optional
from lexer import *


# AST aka -> JSONValue
@dataclass
class AST:
    pass

@dataclass
class JSONObject(AST):
    members: Dict[str, AST]
    
    def __getattr__(self, attr):
        return self.members[attr]
    
@dataclass
class JSONArray(AST):
    elts: List[AST]
    
    def __getitem__(self, i):
        return self.elts[i]

# @dataclass
# class JSONString(AST):
#     val: str
#     def __repr__(self):
#         return self.val


def parse(s: str) -> AST:
    t = peekable(lex(s))
    i = 0
    
    def peek():
        return t.peek(None)
    
    def consume(expected_type: Optional[type] = None, expected_val: Optional[str] = None) -> Token:
        nonlocal i
        token = next(t, None)
        i += 1
        if token is None:
            raise ValueError(f"Unexpected end of input at index {i}")
        if expected_type and not isinstance(token, expected_type):
            raise ValueError(f"Expected token type {expected_type.__name__} at index {i}, but got {type(token).__name__}")
        if expected_val and getattr(token, 'sym', None) != expected_val:
            raise ValueError(f"Expected token value '{expected_val}' at index {i}, but got '{getattr(token, 'sym', None)}'")
        return token
    
    def parse_value():
        token = peek()
        match token:
            case SpecialToken('{'):
                return parse_object()
            case SpecialToken('['):
                return parse_array()
            
            case StringToken(_):
                token = consume(StringToken)
                # return JSONString(token.val)
                return token.val
        
            case NumberToken(_):
                token = consume(NumberToken)
                num_str = token.val
                if '.' in num_str or 'e' in num_str or 'E' in num_str:
                    return float(num_str)
                else:
                    return int(num_str)
            
            case TrueToken():
                consume(TrueToken)
                return True
            
            case FalseToken():
                consume(FalseToken)
                return False
            
            case NullToken():
                consume(NullToken)
                return None
            
            case _:
                raise ValueError(f"Unexpected token at index {i}: {token}")
    
    def parse_object():
        members = {}
        consume(SpecialToken, '{')
        while True:
            token = peek()
            match peek():
                case SpecialToken('}'):
                    consume(SpecialToken, '}')
                    return JSONObject(members)
                case StringToken(key):
                    consume(StringToken)
                    consume(SpecialToken, ':')
                    members[key] = parse_value()
                    match peek():
                        case SpecialToken(','):
                            consume(SpecialToken, ',')
                case _:
                    raise ValueError(f"Expected ',' or '}}' at index {i}, but got {token}")
        
    def parse_array():
        elts = []
        consume(SpecialToken, '[')
        while True:
            token = peek()
            match token:
                case SpecialToken(']'):
                    consume(SpecialToken, ']')
                    return JSONArray(elts)
                case _:
                    if not elts:
                        elts.append(parse_value())
                    else:
                        consume(SpecialToken, ',')
                        elts.append(parse_value())
        
    
    return parse_value()