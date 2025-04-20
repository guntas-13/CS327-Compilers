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

# run_test '{"temperature": -42}' '-42' 'top.temperature'
# run_test '{"matrix": [[1, 2], [3, 4]]}' '4' 'top.matrix[1][1]'
# run_test '{"groups": [{"members": ["Alice", "Bob"]}]}' 'Bob' 'top.groups[0].members[1]'   <- my internal param is named "members"
# run_test '{"a":{"b":{"c":{"d":{"e":"end"}}}}}' 'end' 'top.a.b.c.d.e'
# run_test '{"quote": "She said, \"Yes!\""}' 'She said, "Yes!"' 'top.quote'
# run_test '{"text": "Line1\nLine2\tTabbed"}' 'Line1
# Line2   Tabbed' 'top.text'                                                      <- Actual
# run_test '{"text": "Line1\\nLine2\\tTabbed"}' 'Line1\nLine2\tTabbed' 'top.text' <- intended!
# run_test '{"empty_obj": {}, "empty_arr": []}' '{}' 'top.empty_obj'              -> all have their own reprs!!
# run_test '{"json": [123, {"a": 1}]}' '1' 'top.json[1].a'
# run_test '{"list": [1, 2]}' 'ERROR' 'top.list[5]'
# run_test '{"value": 10}' 'ERROR' 'top.value[0]'
# run_test '{"ok": true}' 'ERROR' 'top.ok.a.b'
# run_test '{"data": [1, 2, 3]}' 'ERROR' 'top.data[-1]' -> Only this is the error!

# run_test '{ // Comment line 
# "name": "Test"}' 'Test' 'top.name'
# run_test '{"active": true, "deleted": false}' 'false' 'top.deleted'
# run_test '{"nums": [1, 2,], "info": {"ok": true,}}' '1' 'top.nums[0]'
# run_test '{"mix": [{"a":1,}, {"b":2,}]}' '2' 'top.mix[1].b'
# run_test '{"arr": [1, 2, 3,]}' '3' 'top.arr[2]'
# run_test '{"map": {"x": {"y": {"z":42,},},},}' '42' 'top.map.x.y.z'
# run_test '{"x": 1 
# // trailing comment
# }' '1' 'top.x'
# run_test '{ "unicode": "Hello \\u0041\\u0042\\u0043"}' 'Hello ABC' 'top.unicode' -> Original
# run_test '{ "unicode": "Hello \u0041\u0042\u0043"}' 'Hello ABC' 'top.unicode' -> correct!
# run_test '{"weird": "comma , inside string"}' 'comma , inside string' 'top.weird'
# run_test '[{ "user": "A"},]' 'A' 'top[0].user'
# run_test '{"nums": [1,,2]}' 'ERROR' 'top.nums[1]'
# run_test '{"obj": {"a": 1,, "b": 2}}' 'ERROR' 'top.obj.b'