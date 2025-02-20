#!/usr/bin/env bash

run_test() {
    if [ $# -ne 3 ]; then
        echo "Usage: run_test <input_data> <expected_output> <unused_arg>"
        return 1
    fi
    
    printf "%s\n" "$1" > input.json
    printf "%s\n" "$2" > expected.txt
    ./run.sh "$3" input.json > actual_output.txt
    diff actual_output.txt expected.txt
    rm input.json expected.txt actual_output.txt
}

run_test '{
    "name": "Alice",
    "age": 30,
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}' 'Alice' 'top.name'

run_test '{
    "products": [
        {
            "id": 1,
            "name": "Laptop",
            "price": 999.99
        },
        {
            "id": 2,
            "name": "Smartphone",
            "price": 499.49
        }
    ]
}' '999.99' 'top.products[0].price'

run_test '{
    "user": {
        "details": {
            "first_name": "John",
            "last_name": "Doe"
        },
        "preferences": {
            "theme": "dark"
        }
    }
}' 'dark' 'top.user.preferences.theme'
