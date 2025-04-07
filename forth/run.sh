#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <file> [args...]"
    exit 1
fi

# Determine the Python executable to use
PYTHON_EXEC=$(command -v python3.11 || command -v python3)

if [ -z "$PYTHON_EXEC" ]; then
    echo "Python 3.11 or Python 3 is not installed."
    exit 1
fi

"$PYTHON_EXEC" test.py "$@"

# Note: On some machines, adjust 'python3.11' or 'python3' to match the installed Python version (>3.10).