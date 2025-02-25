def f():
    return 6

def f(a):
    return a + 5

# print(f(f())) -> Error since Function Overloading is not supported in Python! 
# [Not even on the basis of number of arguments]
print(f(3))