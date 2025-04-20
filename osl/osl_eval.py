from osl_parser import *

def e(tree: AST, env: Environment = None) -> int | float | bool:
    if env is None:
        env = Environment()
        
    def e_(tree: AST):
        return e(tree, env)
    
    match tree:
        case Program(decls):
            res = None
            for decl in decls:
                res = e_(decl)
            return res
        
        case Number(val):
            return val
        
        case StringLiteral(val):
            return val
        
        case Variable(varName, i):
            return env.get(f"{varName}:{i}")
        
        case Let(Variable(varName, i), e1):
            v1 = e_(e1) if e1 else None
            env.add(f"{varName}:{i}", v1)
            return None
        
        case Assign(Variable(varName, i), e1):
            v1 = e_(e1)
            env.update(f"{varName}:{i}", v1)
            return None
        
        case LetFun(Variable(varName, i), params, body):
            # Closure -> Copy of Environment taken along with the declaration!
            funObj = FunObj(params, body, None)
            env.add(f"{varName}:{i}", funObj)
            funObj.env = env
            return None
        
        case CallFun(fn, args):
            if isinstance(fn, Variable):
                fun = env.get(f"{fn.varName}:{fn.id}")
                rargs = [e_(arg) for arg in args]
                
                # use the environment that was copied when the function was defined
                call_env = fun.env.copy()
                call_env.enter_scope()
                for param, arg in zip(fun.params, rargs):
                    call_env.add(f"{param.varName}:{param.id}", arg)
                
                rbody = e(fun.body, call_env)
                # print("#"*50)
                # print(rbody)
                # print("#"*50)
                return rbody
            else:
                if isinstance(fn, CallFun):
                    fun = e_(fn)
                    # fun = env.get(f"{fnvar.÷varName}:{fnvar.id}")
                    rargs = [e_(arg) for arg in args]
                    
                    # use the environment that was copied when the function was defined
                    call_env = fun.env.copy()
                    call_env.enter_scope()
                    for param, arg in zip(fun.params, rargs):
                        call_env.add(f"{param.varName}:{param.id}", arg)
                    
                    rbody = e(fun.body, call_env)
                    # print("**"*50)
                    # print(rbody)
                    # print("**"*50)
                    return rbody

        case Arr(arr, size):
            return Arr([e_(elem) for elem in arr], size)
        
        case ArrAccess(arr, index):
            if isinstance(arr, Variable):
                arrNode = env.get(f"{arr.varName}:{arr.id}")
                index = e_(index)
                if isinstance(arrNode, Arr) and 0 <= index < arrNode.size:
                    return arrNode.arr[index]
                else:
                    raise IndexError(f"Index {index} out of bounds for array {arr.varName}")
            
            if isinstance(arr, ArrAccess):
                arrNode = e_(arr)
                index = e_(index)
                if isinstance(arrNode, Arr) and 0 <= index < arrNode.size:
                    return arrNode.arr[index]
                else:
                    raise IndexError(f"Index {index} out of bounds")
        
        case Statements(stmts):
            env.enter_scope()
            res = None
            for i, stmt in enumerate(stmts):
                res = e_(stmt)
                if res is not None:
                    env.exit_scope()
                    return res
            env.exit_scope()
            return res
        
        case WhileStmt(cond, body):
            while e_(cond):
                res = e_(body)
                if res is not None:
                    return res
            return None
        
        case PrintStmt(expr):
            print(e_(expr))
            return
        
        case ReturnStmt(expr):
            if expr:
                return e_(expr)
            return None
            
        case BinOp("+", left, right): return e_(left) + e_(right)
        case BinOp("*", left, right): return e_(left) * e_(right)
        case BinOp("/", left, right): 
            left_val = e_(left)
            right_val = e_(right)
            if isinstance(left_val, int) and isinstance(right_val, int):
                return left_val // right_val
            return left_val / right_val
        case BinOp("^", left, right): return e_(left) ** e_(right)
        case BinOp("-", left, right): return e_(left) - e_(right)
        case BinOp("<", left, right): return e_(left) < e_(right)
        case BinOp(">", left, right): return e_(left) > e_(right)
        case BinOp("<=", left, right): return e_(left) <= e_(right)
        case BinOp(">=", left, right): return e_(left) >= e_(right)
        case BinOp("=", left, right): return e_(left) == e_(right)
        case BinOp("!=", left, right): return e_(left) != e_(right)
        case BinOp("%", left, right): return e_(left) % e_(right)
        case BinOp("||", left, right): return e_(left) or e_(right)
        case BinOp("&&", left, right): return e_(left) and e_(right)
        
        case UnOp("-", right): return -e_(right)
        case UnOp("\u221a", right): return e_(right) ** 0.5
        
        case If(condition, then_body, else_body): 
            if e_(condition):
                return e_(then_body) 
            else:
                return e_(else_body)
        
        case IfUnM(condition, then_body):
            if e_(condition):
                return e_(then_body)
            return None