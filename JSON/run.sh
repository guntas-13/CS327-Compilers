#!/bin/bash

if command -v python3.11 &> /dev/null
then
    python3.11 main.py $1 $2
elif command -v python3 &> /dev/null
then
    python3 main.py $1 $2
else
    echo "Python 3.11 or Python 3 is not installed."
    exit 1
fi

# on other machines they might need to change this to python3 or python 
# depending on the default python > v3.10 installed on the machine.