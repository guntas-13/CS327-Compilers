from calculator_extended import parse, e, resolve
from pprint import pprint

def unit_test(expr: str, expected_value, results):
    print(f"Expression: {expr}")
    try:
        ast = parse(expr)
        pprint(ast)
        result = e(ast)
        print(f"Evaluated Result: {result}")
        if result != expected_value:
            error_msg = f"Test failed for expression: {expr}. Expected {expected_value}, but got {result}."
            results.append(("FAILED", expr, error_msg))
            print(error_msg)
            print()
        else:
            results.append(("PASSED", expr, None))
            print("Test passed!\n")
    except Exception as ep:
        error_msg = f"Error evaluating expression: {expr}. Exception: {ep}"
        results.append(("ERROR", expr, error_msg))
        print(error_msg)
        print()

log = []

unit_test("2", 2, log)
unit_test("2+3", 5, log)
unit_test("2+3*5", 17, log)
unit_test("2 + 3*5", 17, log)
unit_test("2 + 3*5^2", 77, log)
unit_test("2 + 3*5^2 - 3", 74, log)
unit_test("2 + 3*5^2 - 3 / 2", 75.5, log)
unit_test("2.5 + 3.5", 6.0, log)
unit_test("2^3^2", 512, log)
unit_test("2.5^3^2", 3814.697265625, log)
unit_test("3 + 2*3.5^4/2", 153.0625, log)
unit_test("2-3-5-6", -12, log)
unit_test("2/3/5", 0.13333333333333333, log)
unit_test("((2+3)*5)/5", 5.0, log)
unit_test("3-(5-6)", 4, log)
unit_test("3*(5-6^3)", -633, log)
unit_test("2- -2", 4, log)
unit_test("2- -(3 - 1)", 4, log)
unit_test("5*-5", -25, log)
unit_test("-5*5", -25, log)
unit_test("2 +-3", -1, log)
unit_test("-(5-2)", -3, log)
unit_test("-((4*5)-(4/5))", -19.2, log)
unit_test("\u221a(4)", 2, log)

exp_sq = "\u221a(4 + 12) + \u221a(9)"
unit_test(exp_sq, 7.0, log)

exp_cond1 = """
if 2 < 3 then
    0 + 5
else
    1 * 6
end
"""
unit_test("if 2 < 3 then 2 else 3 end", 2, log)
unit_test(exp_cond1, 5, log)


exp_cond = """
if 2 < 3 then 
    if 4 > 5 then 
        1 
    else 
        if 6 <= 7 then 
            8 
        else 
            9 
        end 
    end 
else 
    10 
end
"""
unit_test(exp_cond, 8, log)



print("\nTest Summary:")
for status, expr, error_msg in log:
    if status == "PASSED":
        print(f"PASSED: {expr}")
    else:
        print(f"{status}: {expr}")
        if error_msg:
            print(f"  -> {error_msg}")
