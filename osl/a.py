import dis

def foo():
    a = [[1], [2, 3, 4]]
    # p = a[0]
    a[0] = 1

dis.dis(foo)