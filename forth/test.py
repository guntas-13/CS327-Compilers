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

prog7 = """
2 -3 - put
"""

prog8 = """
1 2 3 rot / put
"""

# # dividend - (dividend / divisor) * divisor
# prog9 = """
# "Enter dividend: " put get
# dup
# "Enter divisor: " put get
# / dup * - put
# """


eval(prog8)