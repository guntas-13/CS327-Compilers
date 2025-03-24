from vm import eval

prog1 = """
"Hello, " get "!" concat concat put
"""

prog2 = """
2 3 + put
"""

prog3 = """
get get + put
"""

prog4 = """
10 2 / put
"""

prog5 = """
"Enter first number: " put get
"Enter second number: " put get
"Their sum is: " put + put
"""

prog6 = """
get get concat put
"""

eval(prog6)