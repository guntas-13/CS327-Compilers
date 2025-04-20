from osl_eval import e
from osl_parser import parse, resolve
import time
import sys
from colorama import Fore, Style
# from codegen import *
# from vm import StackVM, Code

sys.setrecursionlimit(100000000)

def run_test(exp, expected, label):
    print(f"\n{label} osl Code:")
    print(exp)
    start_time = time.time()
    result = e(resolve(parse(exp)))
    end_time = time.time() - start_time

    # code = Code(bytecode=result)

    # stack = StackVM(code)
    # t2 = time.time()
    # result = stack.execute()
    # t1 = time.time() - t2
    print(f"Expected: {expected}")
    print(f"Result: {result}")
    # print(f"osl compilation Time: {Fore.CYAN}{end_time:.6f} seconds{Style.RESET_ALL}")
    # print(f"osl execution Time: {Fore.CYAN}{t1:.6f} seconds{Style.RESET_ALL}")
    print(f"osl execution Time: {Fore.CYAN}{end_time:.6f} seconds{Style.RESET_ALL}")
    # print(f"osl total Time: {Fore.CYAN}{t1+end_time:.6f} seconds{Style.RESET_ALL}")
    return end_time

# Euler Problem 1: Sum of multiples of 3 or 5
exp1 = """
def F(x, s) {
    while (x < 1000) {
        if (x % 3 = 0 || x % 5 = 0) {
            s := s + x;
        }
        x := x + 1;
    }
    return s;
}
F(0, 0);
"""
t1 = run_test(exp1, 233168, "Problem 1")

def F(x, s):
    while x < 1000:
        if x % 3 == 0 or x % 5 == 0:
            s += x
        x += 1
    return s

start_time = time.time()
py_result1 = F(0, 0)
t2 = time.time() - start_time
print(f"Python Result: {py_result1}")
print(f"Python Time: {Fore.CYAN}{t2:.6f} seconds{Style.RESET_ALL}")
print(f"osl is {int(t1//t2)}x slower than Python")

# Euler Problem 2: Even Fibonacci numbers
exp2 = """
def fib(a, b, s) {
    while (a < 4000000) {
        if (a % 2 = 0) {
            s := s + a;
        }
        var temp := a;
        a := b;
        b := temp + b;
    }
    return s;
}
fib(0, 1, 0);
"""
t1 = run_test(exp2, 4613732, "Problem 2")

def fib(a, b, s):
    while a < 4000000:
        if a % 2 == 0:
            s += a
        a, b = b, a + b
    return s

start_time = time.time()
py_result2 = fib(0, 1, 0)
t2 = time.time() - start_time
print(f"Python Result: {py_result2}")
print(f"Python Time: {Fore.CYAN}{t2:.6f} seconds{Style.RESET_ALL}")
print(f"osl is {int(t1//t2)}x slower than Python")

# Euler Problem 3: Largest prime factor
exp3 = """
def prime(n, i) {
    while (i * i <= n) {
        if (n % i = 0) {
            n := n / i;
        } else {
            i := i + 1;
        }
    }
    return n;
}
var n := 600851475143;
prime(n, 2);
"""
t1 = run_test(exp3, 6857, "Problem 3")

def largest_prime_factor(n, i):
    while i * i <= n:
        if n % i == 0:
            n //= i
        else:
            i += 1
    return n

start_time = time.time()
py_result3 = largest_prime_factor(600851475143, 2)
t2 = time.time() - start_time
print(f"Python Result: {py_result3}")
print(f"Python Time: {Fore.CYAN}{t2:.6f} seconds{Style.RESET_ALL}")
print(f"osl is {int(t1//t2)}x slower than Python")

# Euler Problem 4: Largest palindrome product
# exp4 = """
# def isPal(n, rev, org) {
#     if (n = 0)
#     {
#         if (org = rev) return 1;
#         return 0;
#     }
#     return isPal(n/10, rev*10 + n%10, org);
# }
# def F() {
#     var maxPal := 0;
#     var i := 999;
#     while (i >= 100) {
#         var j := 999;
#         while (j >= 100) {
#             var prod := i * j;
#             if ((prod > maxPal) && (isPal(prod, 0, prod))) {
#                 maxPal := prod;
#             }
#             j := j - 1;
#         }
#         i := i - 1;
#     }
#     return maxPal;
# }
# F();
# """
# t1 = run_test(exp4, 906609, "Problem 4")

# def is_palindrome(n):
#     return str(n) == str(n)[::-1]

# def F():
#     max_pal = 0
#     i = 999
#     while i >= 100:
#         j = 999
#         while j >= 100:
#             prod = i * j
#             if prod > max_pal and is_palindrome(prod):
#                 max_pal = prod
#             j -= 1
#         i -= 1
#     return max_pal

# start_time = time.time()
# py_result4 = F(999, 999, 0)
# t2 = time.time() - start_time
# print(f"Python Result: {py_result4}")
# print(f"Python Time: {Fore.CYAN}{t2:.6f} seconds{Style.RESET_ALL}")
# print(f"osl is {int(t1//t2)}x slower than Python")


# Euler Problem 5: Smallest multiple
exp5 = """
def gcd(a, b) {
    while (b != 0) {
        var temp := b;
        b := a % b;
        a := temp;
    }
    return a;
}
def lcm(a, b) {
    return a * b / gcd(a, b);
}
def F(n, i) {
    while (i > 1) {
        n := lcm(n, i - 1);
        i := i - 1;
    }
    return n;
}
F(1, 20);
"""
t1 = run_test(exp5, 232792560, "Problem 5")

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def F(n, i):
    while i > 1:
        n = lcm(n, i - 1)
        i -= 1
    return n

start_time = time.time()
py_result5 = F(1, 20)
t2 = time.time() - start_time
print(f"Python Result: {py_result5}")
print(f"Python Time: {Fore.CYAN}{t2:.6f} seconds{Style.RESET_ALL}")
print(f"osl is {int(t1//t2)}x slower than Python")

# Euler Problem 6: Sum square difference
exp6 = """
def F(n, sum, sumSq) {
    while (n > 0) {
        sum := sum + n;
        sumSq := sumSq + n * n;
        n := n - 1;
    }
    return sum * sum - sumSq;
}
F(100, 0, 0);
"""
t1 = run_test(exp6, 25164150, "Problem 6")

def F(n, sum, sumSq):
    while n > 0:
        sum += n
        sumSq += n * n
        n -= 1
    return sum * sum - sumSq

start_time = time.time()
py_result6 = F(100, 0, 0)
t2 = time.time() - start_time
print(f"Python Result: {py_result6}")
print(f"Python Time: {Fore.CYAN}{t2:.6f} seconds{Style.RESET_ALL}")
print(f"osl is {int(t1//t2)}x slower than Python")