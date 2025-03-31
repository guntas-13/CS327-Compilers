from osl_eval import *
import struct

class BytecodeGenerator:
    def __init__(self):
        self.bytecode = bytearray()
        self.labels = {}
        self.label_counter = 0

    def emit(self, *bytes):
        """Append bytes to the bytecode."""
        self.bytecode.extend(bytes)

    def emit_int(self, value: int):
        """Emit a 4-byte integer in little-endian format with PUSH_INT."""
        self.emit(0x03)  # PUSH_INT opcode
        self.emit(*struct.pack('<i', value))  # 4 bytes, little-endian

    def emit_short(self, value: int):
        """Emit a 2-byte signed short in little-endian format (for jumps)."""
        self.emit(*struct.pack('<h', value))  # 2 bytes, little-endian

    def new_label(self):
        """Generate a new label name."""
        self.label_counter += 1
        return f"L{self.label_counter}"

    def place_label(self, label: str):
        """Mark the current position as a label."""
        self.labels[label] = len(self.bytecode)

    def resolve_jumps(self):
        """Resolve all jump offsets after bytecode generation."""
        i = 0
        while i < len(self.bytecode):
            opcode = self.bytecode[i]
            if opcode in {0x50, 0x51, 0x52}:  # JUMP, JUMP_IF_ZERO, JUMP_IF_NONZERO
                # Extract the label placeholder (2 bytes after opcode)
                label_idx = i + 1
                label_num = struct.unpack('<h', self.bytecode[label_idx:label_idx+2])[0]
                label = f"L{label_num}"
                if label in self.labels:
                    target = self.labels[label]
                    offset = target - (i + 3)  # Offset relative to post-instruction PC
                    self.bytecode[label_idx:label_idx+2] = struct.pack('<h', offset)
                else:
                    raise ValueError(f"Label {label} not found")
                i += 3
            else:
                i += 1  # Move to next instruction (simplified; actual size varies)

    def generate(self, ast) -> bytearray:
        """Generate bytecode from the AST."""
        self.gen_program(ast)
        self.resolve_jumps()
        return self.bytecode

    def gen_program(self, program):
        """Generate bytecode for a Program node."""
        match program:
            case Program(decls):
                for decl in decls:
                    self.gen_declaration(decl)
                self.emit(0x55)  # HALT

    def gen_declaration(self, decl):
        """Generate bytecode for a declaration (let, statement, etc.)."""
        match decl:
            case Let(var, e1):
                if e1:
                    self.gen_expression(e1)
                    # For now, we leave the value on the stack (no variable storage)
            case Assign(var, e1):
                self.gen_expression(e1)
                # For now, leave on stack (no variable update in VM yet)
            case LetFun(name, params, body):
                # Stub for function definition
                pass  # Not implemented yet
            case _:
                self.gen_statement(decl)

    def gen_statement(self, stmt):
        """Generate bytecode for a statement."""
        match stmt:
            case PrintStmt(expr):
                self.gen_expression(expr)
                # VM doesn't have print; leave value on stack for now
            case ReturnStmt(expr):
                if expr:
                    self.gen_expression(expr)
                # No RETURN handling yet; leave value on stack
            case Statements(stmts):
                for s in stmts:
                    self.gen_statement(s)
            case If(condition, then_body, else_body):
                self.gen_if(condition, then_body, else_body)
            case IfUnM(condition, then_body):
                self.gen_if(condition, then_body, None)
            case _:
                self.gen_expression(stmt)

    def gen_if(self, condition, then_body, else_body):
        """Generate bytecode for if statements."""
        else_label = self.new_label()
        end_label = self.new_label() if else_body else else_label

        # Evaluate condition
        self.gen_expression(condition)
        self.emit(0x51)  # JUMP_IF_ZERO
        self.emit_short(int(else_label[1:]))  # Placeholder for label number

        # Then branch
        self.gen_statement(then_body)
        if else_body:
            self.emit(0x50)  # JUMP to end
            self.emit_short(int(end_label[1:]))  # Placeholder

        self.place_label(else_label)
        if else_body:
            self.gen_statement(else_body)
            self.place_label(end_label)

    def gen_expression(self, expr):
        """Generate bytecode for an expression."""
        match expr:
            case Number(val):
                self.emit_int(int(val))  # Assuming all numbers are integers
            case Variable(varName, id):
                # For now, no variable lookup; assume value is already on stack
                pass
            case BinOp(op, left, right):
                self.gen_binop(op, left, right)
            case UnOp(op, right):
                self.gen_unop(op, right)
            case CallFun(fn, args):
                # Stub for function call
                pass  # Not implemented yet
            case _:
                raise ValueError(f"Unsupported expression: {expr}")

    def gen_binop(self, op: str, left, right):
        """Generate bytecode for binary operations."""
        self.gen_expression(left)
        self.gen_expression(right)
        opcodes = {
            '+': 0x20,  # ADD
            '-': 0x21,  # SUB
            '*': 0x22,  # MUL
            '/': 0x23,  # DIV
            '%': 0x24,  # MOD
            '<': 0x42,  # LT
            '>': 0x43,  # GT
            '<=': 0x44, # LE
            '>=': 0x45, # GE
            '=': 0x40,  # EQ
            '!=': 0x41, # NEQ
            '&&': None, # Logical AND (requires control flow)
            '||': None, # Logical OR (requires control flow)
            '^': None   # Exponentiation (not directly supported)
        }
        if op in opcodes and opcodes[op] is not None:
            self.emit(opcodes[op])
        elif op == '&&':
            # Short-circuit AND using jumps
            end_label = self.new_label()
            false_label = self.new_label()
            self.emit(0x51)  # JUMP_IF_ZERO
            self.emit_short(int(false_label[1:]))
            self.gen_expression(right)
            self.emit(0x51)  # JUMP_IF_ZERO
            self.emit_short(int(false_label[1:]))
            self.emit_int(1)  # Push true
            self.emit(0x50)  # JUMP to end
            self.emit_short(int(end_label[1:]))
            self.place_label(false_label)
            self.emit_int(0)  # Push false
            self.place_label(end_label)
        elif op == '||':
            # Short-circuit OR using jumps
            end_label = self.new_label()
            true_label = self.new_label()
            self.emit(0x52)  # JUMP_IF_NONZERO
            self.emit_short(int(true_label[1:]))
            self.gen_expression(right)
            self.emit(0x52)  # JUMP_IF_NONZERO
            self.emit_short(int(true_label[1:]))
            self.emit_int(0)  # Push false
            self.emit(0x50)  # JUMP to end
            self.emit_short(int(end_label[1:]))
            self.place_label(true_label)
            self.emit_int(1)  # Push true
            self.place_label(end_label)
        else:
            raise ValueError(f"Operation {op} not supported yet")

    def gen_unop(self, op: str, right):
        """Generate bytecode for unary operations."""
        self.gen_expression(right)
        if op == '-':
            self.emit(0x25)  # NEG
        elif op == '\u221a':  # Square root
            # Not directly supported; approximate or skip
            pass
        else:
            raise ValueError(f"Unary operation {op} not supported")

# Example usage with your parser
def compile_to_bytecode(source: str) -> bytearray:
    ast = parse(source)
    resolved_ast = resolve(ast)
    generator = BytecodeGenerator()
    return generator.generate(resolved_ast)

# Test with one of your examples
source = """
var x := 5;
x := x + 6;
x;
"""

source = """
var x := 5;
if (x < 10)
{
    x;  
} 
else
{
    x + 1;   
}
"""
bytecode = compile_to_bytecode(source)
print([hex(b) for b in bytecode])