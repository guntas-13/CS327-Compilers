from calculator_extended_resolved import parse, e, resolve
from pprint import pprint
from colorama import Fore, Style

def unit_test(expr: str, expected_value: str, results):
    print(f"Expression: {expr}")
    try:
        ast = resolve(parse(expr))
        # ast = parse(expr)
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
        results.append(("ERROR", expr, f"{Fore.RED}{error_msg}{Style.RESET_ALL}"))
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

exp = """
var x := 5;
letFunc f(y) 
{
    return x;
} 
print(x);
print(f(2));
letFunc g(z) 
{ 
    var x := 6;
    return f(z);
}
g(0);
"""

unit_test(exp, 5, log)

exp = """
var x := 5;
letFunc f(y) 
{
    return y ^ 2;
}
{
    var x := 6;
    return f(x);
}
print(f(x));
print(x);
letFunc g(z)
{
    return f(z);
}
print(f(g(2)));
print(g(3));
"""

exp = """
letFunc f1()
{
    letFunc f2()
    {
        var x := 10;
        return x;
    }
    return f2;
}
var msg := f1();
msg();
"""

exp = """
letFunc f1()
{
    var x := 10;
    letFunc f2()
    {
        return x;
    }
    return f2;
}
var msg := f1();
msg();
"""

exp = """
var x := 6;

letFunc F(x)
{
    letFunc G()
    {
        return x;
    }
    return G;
}

var y := F(5);
y() * y();
"""

exp = """
var x := 15;
if (x > 10)
if (x < 20)
print(x + 1);
else print(x - 1);
x;
"""

exp = """
letFunc fact(n)
{
    if (n = 0)
        return 1;
    return n * fact(n - 1);
}
fact(5);
"""

print("\nTest Summary:")
passed_count = 0
for status, expr, error_msg in log:
    if status == "PASSED":
        print(f"{Fore.GREEN}PASSED: {expr}{Style.RESET_ALL}")
        passed_count += 1
    else:
        print(f"{Fore.RED}{status}: {expr}{Style.RESET_ALL}")
        if error_msg:
            print(f"  -> {error_msg}")

print(f"\nTotal Passed: {passed_count} out of {len(log)}")
