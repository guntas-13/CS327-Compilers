#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

# Try python3.11 first, then python3
if command -v python3.11 &> /dev/null; then
    python3.11 test.py "$1"
elif command -v python3 &> /dev/null; then
    python3 test.py "$1"
else
    echo "Python 3.11 or Python 3 is not installed."
    exit 1
fi

# Note: On some machines, adjust 'python3.11' or 'python3' to match the installed Python version (>3.10).