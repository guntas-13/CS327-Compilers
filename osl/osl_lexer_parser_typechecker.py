from collections.abc import Iterator
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple
from more_itertools import peekable

# --- Lexer ---
class Token:
    pass

@dataclass
class NumberToken(Token):
    val: str

@dataclass
class OperatorToken(Token):
    op: str
    
@dataclass
class KeyWordToken(Token):
    op: str
    
@dataclass
class VariableToken(Token):
    varName: str

@dataclass
class StringToken(Token):
    val: str

@dataclass
class FunCallToken(Token):
    funName: str

@dataclass
class TypeToken(Token):
    type: str

@dataclass
class BoolToken(Token):
    val: str

def lex(s: str) -> Iterator[Token]:
    i = 0
    prev_token = None

    while True:
        while i < len(s) and s[i].isspace():
            i += 1

        if i >= len(s):
            return

        if s[i].isalpha() or s[i] == '_':
            start = i
            while i < len(s) and (s[i].isalpha() or s[i].isdigit() or s[i] == '_'):
                i += 1
            name = s[start:i]

            if name in {"if", "else", "var", "in", "fn", "log", "return"}:
                prev_token = KeyWordToken(name)
                yield prev_token
            elif name in {"bool", "i8", "i16", "i32", "i64", "i128", "u8", "u16", "u32", "u64", "u128",
                          "f8", "f16", "f32", "f64", "f128", "c8"}:
                prev_token = TypeToken(name)
                yield prev_token
            elif name in {"true", "false"}:
                prev_token = BoolToken(name)
                yield prev_token
            elif isinstance(prev_token, KeyWordToken) and prev_token.op == "fn":
                prev_token = VariableToken(name)
                yield prev_token
            elif i < len(s) and s[i] == "(":
                prev_token = FunCallToken(name)
                yield prev_token
            else:
                prev_token = VariableToken(name)
                yield prev_token

        elif s[i] == '/' and i + 1 < len(s) and s[i + 1] == '/':
            i += 2
            while i < len(s) and s[i] != '\n':
                i += 1

        elif s[i] == '"':
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

        elif s[i].isdigit() or (s[i] == '0' and i + 1 < len(s) and s[i + 1] in 'boxBOX'):
            start = i
            base = 10
            if s[i] == '0' and i + 1 < len(s):
                if s[i + 1] in 'bB':
                    base = 2
                    i += 2
                    start = i
                    while i < len(s) and s[i] in '01':
                        i += 1
                elif s[i + 1] in 'oO':
                    base = 8
                    i += 2
                    start = i
                    while i < len(s) and s[i] in '01234567':
                        i += 1
                elif s[i + 1] in 'xX':
                    base = 16
                    i += 2
                    start = i
                    while i < len(s) and s[i] in '0123456789abcdefABCDEF':
                        i += 1
                else:
                    while i < len(s) and s[i].isdigit():
                        i += 1
            else:
                while i < len(s) and s[i].isdigit():
                    i += 1

            if i < len(s) and s[i] == '.':
                i += 1
                while i < len(s) and (
                    (base == 2 and s[i] in '01') or
                    (base == 8 and s[i] in '01234567') or
                    (base == 10 and s[i].isdigit()) or
                    (base == 16 and s[i] in '0123456789abcdefABCDEF')
                ):
                    i += 1

            if i < len(s) and s[i] in 'eEpP':
                i += 1
                if i < len(s) and s[i] in '+-':
                    i += 1
                while i < len(s) and (
                    (base == 2 and s[i] in '01') or
                    (base == 8 and s[i] in '01234567') or
                    (base == 10 and s[i].isdigit()) or
                    (base == 16 and s[i] in '0123456789abcdefABCDEF')
                ):
                    i += 1

            number_str = s[start:i]
            prev_token = NumberToken(number_str)
            yield prev_token

        else:
            if s[i:i+2] in {"<=", ">=", "!=", "||", "&&", ":="}:
                prev_token = OperatorToken(s[i:i+2])
                yield prev_token
                i += 2
            elif s[i] in {'+', '*', '/', '^', '-', '(', ')', '<', '>', '=', '%', '\u221a', ",", "{", "}", ";", ":"}:
                prev_token = OperatorToken(s[i])
                yield prev_token
                i += 1
            else:
                raise ParseErr(f"Unexpected character: {s[i]} at position {i}")

# --- Environment and AST ---
class Environment:
    envs: List[Dict[str, tuple[int, str]]]  # (id, type)
    funcs: Dict[str, 'LetFun']  # Function name to LetFun node
    
    def __init__(self):
        self.envs = [{}]
        self.funcs = {}
    
    def enter_scope(self):
        self.envs.append({})
    
    def exit_scope(self):
        assert self.envs
        self.envs.pop()
    
    def add(self, var: str, id: int, type: str):
        assert var not in self.envs[-1], f"Variable {var} already defined"
        self.envs[-1][var] = (id, type)
    
    def get(self, var: str) -> tuple[int, str]:
        for env in reversed(self.envs):
            if var in env:
                return env[var]
        raise ValueError(f"Variable {var} not defined")
    
    def update(self, var: str, id: int, type: str):
        for env in reversed(self.envs):
            if var in env:
                env[var] = (id, type)
                return
        raise ValueError(f"Variable {var} not defined")
    
    def add_func(self, name: str, func: 'LetFun'):
        assert name not in self.funcs, f"Function {name} already defined"
        self.funcs[name] = func
    
    def get_func(self, name: str) -> 'LetFun':
        return self.funcs.get(name)
    
    def copy(self):
        new_env = Environment()
        new_env.envs = [dict(scope) for scope in self.envs]
        new_env.funcs = dict(self.funcs)
        return new_env

@dataclass
class AST:
    pass

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST

@dataclass
class Number(AST):
    val: str

@dataclass
class UnOp(AST):
    op: str
    right: AST
    
@dataclass
class If(AST):
    condition: AST
    then_body: AST
    else_body: AST

@dataclass
class IfUnM(AST):
    condition: AST
    then_body: AST

@dataclass
class Let(AST):
    var: 'Variable'
    type: str  # Mandatory
    e1: Optional[AST]

@dataclass
class Assign(AST):
    var: 'Variable'
    e1: AST

@dataclass
class Variable(AST):
    varName: str
    type: str  # Mandatory
    id: Optional[int] = None

@dataclass
class LetFun(AST):
    name: 'Variable'
    params: List['Variable']
    return_type: str  # Mandatory
    body: AST

@dataclass
class CallFun(AST):
    fn: 'Variable'
    args: List[AST]
    
@dataclass
class FunObj:
    params: List['Variable']
    body: AST
    env: Environment
    entry: Optional[int] = None 
    
@dataclass
class Statements(AST):
    stmts: List[AST]
    
@dataclass
class PrintStmt(AST):
    expr: AST
    
@dataclass
class ReturnStmt(AST):
    expr: Optional[AST]
    
@dataclass
class Program(AST):
    decls: List[AST]

@dataclass
class StringLiteral(AST):
    val: str

@dataclass
class BoolLiteral(AST):
    val: bool

class ParseErr(Exception):
    pass

class TypeErr(Exception):
    pass

# --- Parser ---
cnt = 0
def fresh():
    global cnt
    cnt += 1
    return cnt

def parse(s: str) -> AST:
    t = peekable(lex(s))
    i = 0
    
    def consume(expected_type=None, expected_value=None):
        nonlocal i
        token = next(t, None)
        if token is None:
            raise ParseErr(f"Unexpected end of input at index {i}")
        if expected_type and not isinstance(token, expected_type):
            raise ParseErr(f"Expected {expected_type.__name__} at index {i}, got {type(token).__name__}")
        if expected_value:
            actual_value = getattr(token, "op", None) or getattr(token, "varName", None) or getattr(token, "val", None) or getattr(token, "type", None)
            if actual_value != expected_value:
                raise ParseErr(f"Expected '{expected_value}' at index {i}, got '{actual_value}'")
        i += 1
        return token
    
    def peek():
        return t.peek(None)
    
    def parse_program():
        decls = []
        while peek():
            decls.append(parse_declaration())
        return Program(decls)
    
    def parse_declaration():
        match peek():
            case KeyWordToken("fn"):
                return parse_func()
            case KeyWordToken("var"):
                return parse_let()
            case _:
                return parse_statement()
            
    def parse_func():
        consume(KeyWordToken, "fn")
        func_name = consume(VariableToken)
        
        consume(OperatorToken, "(")
        params = []
        if peek() != OperatorToken(")"):
            while True:
                param_name = consume(VariableToken).varName
                consume(OperatorToken, ":")
                param_type = consume(TypeToken).type
                params.append(Variable(param_name, param_type))
                if peek() == OperatorToken(","):
                    consume(OperatorToken, ",")
                else:
                    break
        consume(OperatorToken, ")")
        
        consume(OperatorToken, ":")
        return_type = consume(TypeToken).type
        
        body = parse_block()
        return LetFun(Variable(func_name.varName, return_type), params, return_type, body)
    
    def parse_let():
        consume(KeyWordToken, "var")
        var_name = consume(VariableToken).varName
        consume(OperatorToken, ":")
        var_type = consume(TypeToken).type
        e1 = None
        if peek() == OperatorToken(":="):
            consume(OperatorToken, ":=")
            e1 = parse_expression()
        consume(OperatorToken, ";")
        return Let(Variable(var_name, var_type), var_type, e1)
    
    def parse_statement():
        match peek():
            case KeyWordToken("if"):
                return parse_if()
            case KeyWordToken("log"):
                consume(KeyWordToken, "log")
                expr = parse_expression()
                consume(OperatorToken, ";")
                return PrintStmt(expr)
            case KeyWordToken("return"):
                consume(KeyWordToken, "return")
                expr = parse_expression() if peek() != OperatorToken(";") else None
                consume(OperatorToken, ";")
                return ReturnStmt(expr)
            case OperatorToken("{"):
                return parse_block()
            case _:
                expr = parse_expression()
                consume(OperatorToken, ";")
                return expr
        
    def parse_if():
        consume(KeyWordToken, "if")
        condition = parse_expression()
        then_body = parse_statement()
        if peek() == KeyWordToken("else"):
            consume(KeyWordToken, "else")
            else_body = parse_statement()
            return If(condition, then_body, else_body)
        return IfUnM(condition, then_body)
    
    def parse_block():
        consume(OperatorToken, "{")
        decls = []
        while peek() != OperatorToken("}"):
            decls.append(parse_declaration())
        consume(OperatorToken, "}")
        return Statements(decls) if decls else Statements([])
    
    def parse_expression():
        ast = parse_bool()
        if not isinstance(ast, Variable) and peek() == OperatorToken(":="):
            raise ParseErr(f"Expected variable on left side of := at index {i}")
        if isinstance(ast, Variable) and peek() == OperatorToken(":="):
            consume(OperatorToken, ":=")
            e1 = parse_bool()
            return Assign(ast, e1)
        return ast
    
    def parse_bool():
        ast = parse_comparison()
        while True:
            match peek():
                case OperatorToken("||"):
                    consume()
                    ast = BinOp("||", ast, parse_comparison())
                case OperatorToken("&&"):
                    consume()
                    ast = BinOp("&&", ast, parse_comparison())
                case _:
                    return ast

    def parse_comparison():
        ast = parse_add()
        match peek():
            case OperatorToken(op) if op in {"<", ">", "<=", ">=", "=", "!="}:
                consume()
                return BinOp(op, ast, parse_add())
            case _:
                return ast
    
    def parse_add():
        ast = parse_mul()
        while True:
            match peek():
                case OperatorToken('+'):
                    consume()
                    ast = BinOp('+', ast, parse_mul())
                case OperatorToken('-'):
                    consume()
                    ast = BinOp('-', ast, parse_mul())
                case _:
                    return ast
 
    def parse_mul():
        ast = parse_exponentiation()
        while True:
            match peek():
                case OperatorToken('*'):
                    consume()
                    ast = BinOp("*", ast, parse_exponentiation())
                case OperatorToken('/'):
                    consume()
                    ast = BinOp("/", ast, parse_exponentiation())
                case OperatorToken("%"):
                    consume()
                    ast = BinOp("%", ast, parse_exponentiation())
                case _:
                    return ast
    
    def parse_exponentiation():
        ast = parse_atom()
        while True:
            match peek():
                case OperatorToken('^'):
                    consume()
                    ast = BinOp("^", ast, parse_exponentiation())
                case _:
                    return ast

    def parse_atom():
        match peek():
            case NumberToken(v):
                consume()
                return Number(v)
            case BoolToken(v):
                consume()
                return BoolLiteral(v == "true")
            case StringToken(v):
                consume()
                return StringLiteral(v)
            case VariableToken(varName):
                consume()
                return Variable(varName, "unknown")  # Type inferred later
            case FunCallToken(_):
                fn_name = consume(FunCallToken).funName
                consume(OperatorToken, "(")
                args = []
                if peek() != OperatorToken(")"):
                    while True:
                        args.append(parse_expression())
                        if peek() == OperatorToken(","):
                            consume(OperatorToken, ",")
                        else:
                            break
                consume(OperatorToken, ")")
                return CallFun(Variable(fn_name, "unknown"), args)
            case OperatorToken('-'):
                consume()
                return UnOp("-", parse_atom())
            case OperatorToken('\u221a'):
                consume()
                return UnOp("\u221a", parse_atom())
            case OperatorToken("("):
                consume()
                ast = parse_expression()
                consume(OperatorToken, ")")
                return ast
            case _:
                raise ParseErr(f"Unexpected token at index {i}")

    return parse_program()

# --- Resolver ---
def resolve(program: AST, env: Environment = None) -> Tuple[AST, Environment]:
    if env is None:
        env = Environment()
    
    def resolve_(program: AST) -> AST:
        a , _ = resolve(program, env)
        return a

    match program:
        case Program(decls):
            new_decls = [resolve_(decl) for decl in decls]
            return Program(new_decls), env
        
        case Variable(varName, "unknown", None):
            id, type = env.get(varName)
            return Variable(varName, type, id), env
        
        case Variable(varName, type, None):
            id, _ = env.get(varName)
            return Variable(varName, type, id), env
        
        case Number(_) as N:
            return N, env
        
        case BoolLiteral(_) as B:
            return B, env
        
        case StringLiteral(_) as S:
            return S, env
        
        case Let(Variable(varName, var_type, _), _, e1):
            re1 = resolve_(e1) if e1 else (None, env)
            env.add(varName, i := fresh(), var_type)
            return Let(Variable(varName, var_type, i), var_type, re1), env
        
        case Assign(Variable(varName, var_type, _), e1):
            re1 = resolve_(e1)
            id, _ = env.get(varName)
            return Assign(Variable(varName, var_type, id), re1), env
        
        case LetFun(Variable(varName, _, _), params, return_type, body):
            env.add(varName, i := fresh(), return_type)
            env.add_func(varName, LetFun(Variable(varName, return_type, i), params, return_type, body))
            env.enter_scope()
            new_params = []
            for param in params:
                env.add(param.varName, j := fresh(), param.type)
                new_params.append(Variable(param.varName, param.type, j))
            new_body = resolve_(body)
            env.exit_scope()
            return LetFun(Variable(varName, return_type, i), new_params, return_type, new_body), env
        
        case Statements(stmts):
            env.enter_scope()
            stmts = [resolve_(stmt) for stmt in stmts]
            env.exit_scope()
            return Statements([stmt for stmt in stmts]), env
        
        case CallFun(fn, args):
            rfn = resolve_(fn)
            rargs = [resolve_(arg) for arg in args]
            return CallFun(rfn, [arg for arg in rargs]), env
        
        case BinOp(op, left, right):
            le = resolve_(left)
            ri = resolve_(right)
            return BinOp(op, le, ri), env
        
        case UnOp(op, right):
            ri = resolve_(right)
            return UnOp(op, ri), env
        
        case If(condition, then_body, else_body):
            condition = resolve_(condition)
            then_body = resolve_(then_body)
            else_body = resolve_(else_body)
            return If(condition, then_body, else_body), env
        
        case IfUnM(condition, then_body):
            condition = resolve_(condition)
            then_body = resolve_(then_body)
            return IfUnM(condition, then_body), env
        
        case PrintStmt(expr):
            expr = resolve_(expr)
            return PrintStmt(expr), env
        
        case ReturnStmt(expr):
            expr = resolve_(expr) if expr else (None, env)
            return ReturnStmt(expr), env

# --- Type Checker ---
NUMERIC_TYPES = {"i8": 8, "i16": 16, "i32": 32, "i64": 64, "i128": 128,
                 "u8": 8, "u16": 16, "u32": 32, "u64": 64, "u128": 128,
                 "f8": 8, "f16": 16, "f32": 32, "f64": 64, "f128": 128}
SIGNED_INT_TYPES = {"i8": (-128, 127), "i16": (-32768, 32767), "i32": (-2147483648, 2147483647),
                    "i64": (-2**63, 2**63-1), "i128": (-2**127, 2**127-1)}
UNSIGNED_INT_TYPES = {"u8": (0, 255), "u16": (0, 65535), "u32": (0, 4294967295),
                      "u64": (0, 2**64-1), "u128": (0, 2**128-1)}
FLOAT_TYPES = {"f8": 8, "f16": 16, "f32": 32, "f64": 64, "f128": 128}

def get_min_type_for_int(val: int) -> str:
    for type, (min_val, max_val) in SIGNED_INT_TYPES.items():
        if min_val <= val <= max_val:
            return type
    raise TypeErr(f"Integer {val} too large for supported types")

def get_min_type_for_float(val: float) -> str:
    return "f32"  # Simplified; could refine based on precision

def max_type(t1: str, t2: str) -> str:
    if t1 == t2:
        return t1
    if t1 in FLOAT_TYPES or t2 in FLOAT_TYPES:
        bits1 = FLOAT_TYPES.get(t1, 0)
        bits2 = FLOAT_TYPES.get(t2, 0)
        return "f" + str(max(bits1, bits2))
    if t1 in UNSIGNED_INT_TYPES and t2 in SIGNED_INT_TYPES:
        return t1 if NUMERIC_TYPES[t1] > NUMERIC_TYPES[t2] else t2
    if t1 in SIGNED_INT_TYPES and t2 in UNSIGNED_INT_TYPES:
        return t2 if NUMERIC_TYPES[t2] > NUMERIC_TYPES[t1] else t1
    bits1 = NUMERIC_TYPES.get(t1, 0)
    bits2 = NUMERIC_TYPES.get(t2, 0)
    return t1 if bits1 >= bits2 else t2

def can_cast_to(source: str, target: str) -> bool:
    if source == target:
        return True
    if source == "bool" and target == "bool":
        return True
    if source == "c8" and target == "c8":
        return True
    if source in NUMERIC_TYPES and target in NUMERIC_TYPES:
        if source in FLOAT_TYPES and target in FLOAT_TYPES:
            return FLOAT_TYPES[source] <= FLOAT_TYPES[target]
        if source in SIGNED_INT_TYPES and target in SIGNED_INT_TYPES:
            return NUMERIC_TYPES[source] <= NUMERIC_TYPES[target]
        if source in UNSIGNED_INT_TYPES and target in UNSIGNED_INT_TYPES:
            return NUMERIC_TYPES[source] <= NUMERIC_TYPES[target]
        if (source in SIGNED_INT_TYPES or source in UNSIGNED_INT_TYPES) and target in FLOAT_TYPES:
            return True
    return False

def infer_type(ast: AST, env: Environment) -> str:
    match ast:
        case Number(val):
            if val.startswith("0b"):
                n = int(val[2:].replace(".", ""), 2)
                return get_min_type_for_int(n)
            elif val.startswith("0o"):
                n = int(val[2:].replace(".", ""), 8)
                return get_min_type_for_int(n)
            elif val.startswith("0x"):
                n = int(val[2:].replace(".", ""), 16)
                return get_min_type_for_int(n)
            elif "." in val or "e" in val.lower():
                return get_min_type_for_float(float(val))
            else:
                return get_min_type_for_int(int(val))
        
        case BoolLiteral(_):
            return "bool"
        
        case StringLiteral(_):
            return "c8"
        
        case Variable(varName, type, id):
            return type
        
        case BinOp(op, left, right):
            left_type = infer_type(left, env)
            right_type = infer_type(right, env)
            if op in {"+", "-", "*", "/", "%", "^"}:
                if left_type not in NUMERIC_TYPES or right_type not in NUMERIC_TYPES:
                    raise TypeErr(f"Operator {op} requires numeric types, got {left_type} and {right_type}")
                return max_type(left_type, right_type)
            elif op in {"&&", "||"}:
                if left_type != "bool" or right_type != "bool":
                    raise TypeErr(f"Operator {op} requires bool types, got {left_type} and {right_type}")
                return "bool"
            elif op in {"<", ">", "<=", ">=", "=", "!="}:
                if left_type not in NUMERIC_TYPES or right_type not in NUMERIC_TYPES:
                    raise TypeErr(f"Comparison {op} requires numeric types, got {left_type} and {right_type}")
                return "bool"
            raise TypeErr(f"Unknown operator {op}")
        
        case UnOp(op, right):
            right_type = infer_type(right, env)
            if op == "-":
                if right_type not in NUMERIC_TYPES:
                    raise TypeErr(f"Unary - requires numeric type, got {right_type}")
                return right_type
            elif op == "\u221a":
                if right_type not in NUMERIC_TYPES:
                    raise TypeErr(f"Sqrt requires numeric type, got {right_type}")
                return "f32"
            raise TypeErr(f"Unknown unary operator {op}")
        
        case CallFun(fn, args):
            fn_def = env.get_func(fn.varName)
            if not fn_def:
                raise TypeErr(f"Function {fn.varName} not defined")
            if len(args) != len(fn_def.params):
                raise TypeErr(f"Function {fn.varName} expects {len(fn_def.params)} args, got {len(args)}")
            for param, arg in zip(fn_def.params, args):
                arg_type = infer_type(arg, env)
                if not can_cast_to(arg_type, param.type):
                    raise TypeErr(f"Argument type mismatch for {fn.varName}: expected {param.type}, got {arg_type}")
            return fn_def.return_type
        
        case _:
            raise TypeErr(f"Cannot infer type for {ast}")

def typecheck(program: AST, env: Environment) -> None:
    match program:
        case Program(decls):
            for decl in decls:
                typecheck(decl, env)
        
        case Let(var, type, e1):
            if e1:
                e1_type = infer_type(e1, env)
                if not can_cast_to(e1_type, type):
                    raise TypeErr(f"Type mismatch in let {var.varName}: expected {type}, got {e1_type}")
            env.update(var.varName, var.id, type)
        
        case Assign(var, e1):
            e1_type = infer_type(e1, env)
            if not can_cast_to(e1_type, var.type):
                raise TypeErr(f"Type mismatch in assignment to {var.varName}: expected {var.type}, got {e1_type}")
            env.update(var.varName, var.id, var.type)
        
        case LetFun(name, params, return_type, body):
            env.enter_scope()
            for param in params:
                env.add(param.varName, param.id, param.type)
            if isinstance(body, (BinOp, UnOp, Number, BoolLiteral, StringLiteral, Variable, CallFun)):
                body_type = infer_type(body, env)
                if not can_cast_to(body_type, return_type):
                    raise TypeErr(f"Function {name.varName} return type mismatch: expected {return_type}, got {body_type}")
            elif isinstance(body, Statements):
                for stmt in body.stmts:
                    if isinstance(stmt, ReturnStmt) and stmt.expr:
                        expr_type = infer_type(stmt.expr, env)
                        if not can_cast_to(expr_type, return_type):
                            raise TypeErr(f"Return type mismatch in {name.varName}: expected {return_type}, got {expr_type}")
            env.exit_scope()
        
        case Statements(stmts):
            env.enter_scope()
            for stmt in stmts:
                typecheck(stmt, env)
            env.exit_scope()
        
        case If(condition, then_body, else_body):
            cond_type = infer_type(condition, env)
            if cond_type != "bool":
                raise TypeErr(f"If condition must be bool, got {cond_type}")
            typecheck(then_body, env)
            typecheck(else_body, env)
        
        case IfUnM(condition, then_body):
            cond_type = infer_type(condition, env)
            if cond_type != "bool":
                raise TypeErr(f"If condition must be bool, got {cond_type}")
            typecheck(then_body, env)
        
        case PrintStmt(expr):
            infer_type(expr, env)
        
        case ReturnStmt(expr):
            if expr:
                infer_type(expr, env)

test_codes = [
    # Test 1: Basic Arithmetic and Printing
    """
    var a: i32 := 10;
    var b: i32 := 20;
    var c: i64 := a + b;
    log c;
    """,

    # Test 2: Function with Multiple Arguments
    """
    fn multiply(x: i64, y: i64): i64 {
        return x * y;
    }
    var result: i64 := multiply(5, 10);
    log result;
    """,

    # Test 3: Conditional Statements
    """
    var x: i32 := 15;
    var y: i32 := 25;
    var greater: bool := x > y;
    if greater {
        log 1;
    } else {
        log 0;
    }
    """,

    # Test 4: Nested Functions and Scope
    """
    fn add(a: i32, b: i32): i32 {
        return a + b;
    }
    fn double(x: i32): i32 {
        return add(x, x);
    }
    var z: i32 := double(7);
    log z;
    """,

    # Test 5: Mixed Numeric Types
    """
    var small: i8 := 42;
    var medium: i16 := 1000;
    var large: i32 := small + medium;
    var float_val: f32 := 3.14;
    var result: f64 := large + float_val;
    log result;
    """,

    # Test 6: Unary Operations
    """
    var x: i32 := 16;
    var neg: i32 := -x;
    var sqrt: f32 := √x;
    log neg;
    log sqrt;
    """,

    # Test 7: Boolean Operations
    """
    var a: bool := true;
    var b: bool := false;
    var and_result: bool := a && b;
    var or_result: bool := a || b;
    log and_result;
    log or_result;
    """,

    # Test 8: Complex Expression
    """
    var x: i32 := 5;
    var y: i32 := 10;
    var z: i64 := (x + y) * 2;
    fn compute(a: i64): i64 {
        return a + 100;
    }
    var final: i64 := compute(z);
    log final;
    """,

    # Test 9: Empty Function and Block
    """
    fn do_nothing(): i32 {
        var temp: i32 := 0;
        {
            var inner: i32 := 1;
        }
        return temp;
    }
    log do_nothing();
    """,

    # Test 10: String Literal
    """
    var message: c8 := "Hello, world!";
    log message;
    """,

    # Test 11: Type Mismatch (Should Fail)
    """
    var x: i32 := 1000;
    var y: i8 := x;  // i32 cannot safely cast to i8
    log y;
    """,

    # Test 12: Undefined Function (Should Fail)
    """
    log unknown(5);  // unknown function not defined
    """,

    # Test 13: Argument Count Mismatch (Should Fail)
    """
    fn add(a: i32, b: i32): i32 {
        return a + b;
    }
    log add(5);  // Too few arguments
    """,

    # Test 14: Invalid Operator Type (Should Fail)
    """
    var x: bool := true;
    var y: i32 := x + 1;  // Cannot add bool and i32
    log y;
    """
]

# --- Main ---
if __name__ == "__main__":
    for index, code in enumerate(test_codes):
        print(f"\nTesting code #{index + 1}:")
        print("Code:")
        print(code.strip())
        try:
            ast = parse(code)
            resolved_ast, env = resolve(ast)
            typecheck(resolved_ast, env)
            print("Result: Type checking passed!")
        except ParseErr as e:
            print(f"Result: Parse Error: {e}")
        except TypeErr as e:
            print(f"Result: Type Error: {e}")
        except ValueError as e:
            print(f"Result: Value Error: {e}")
        except Exception as e:
            print(f"Result: Unexpected Error: {e}")