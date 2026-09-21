import pprint
import json
import pytest
from smoek.core.data_apis import load_data_from_json, JsonDataPortal

#
# Set data
#


def test_get_DP_int_set():
    dp = load_data_from_json(packed_data={"A": {"set_type": "i", "data": [1, 2, 3]}}, schema="coek")


def test_get_DP_double_set():
    dp = load_data_from_json(
        packed_data={"A": {"set_type": "d", "data": [1.1, 2, 3]}}, schema="coek"
    )
    assert dp["A"] == [1.1, 2.0, 3.0]


def test_get_DP_string_set():
    dp = load_data_from_json(
        packed_data={"A": {"set_type": "s", "data": ["a", "b", "c"]}}, schema="coek"
    )
    assert dp["A"] == ["a", "b", "c"]


def test_get_DP_ituple_set():
    dp = load_data_from_json(
        packed_data={"A": {"set_type": ["i", "i"], "data": [[0, 0], [1, 1], [2, 2]]}},
        schema="coek",
    )
    assert dp["A"] == [(0, 0), (1, 1), (2, 2)]


def test_get_DP_dtuple_set():
    dp = load_data_from_json(
        packed_data={"A": {"set_type": ["d", "d"], "data": [[0, 0], [1.2, 1], [2.3, 2]]}},
        schema="coek",
    )
    assert dp["A"] == [(0.0, 0.0), (1.2, 1.0), (2.3, 2.0)]


def test_get_DP_stuple_set():
    dp = load_data_from_json(
        packed_data={"A": {"set_type": ["s", "s"], "data": [["a", "a"], ["b", "b"], ["c", "c"]]}},
        schema="coek",
    )
    assert dp["A"] == [("a", "a"), ("b", "b"), ("c", "c")]


def test_get_DP_mtuple_set():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "set_type": ["s", "i", "d"],
                "data": [["a", 0, 1], ["b", 1, 2.2], ["c", 2, 3.3]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == [("a", 0, 1.0), ("b", 1, 2.2), ("c", 2, 3.3)]


#
# Parameter data
#


def test_get_DP_int_param():
    dp = load_data_from_json(
        packed_data={"A": 1},
        schema="coek",
    )
    assert dp["A"] == 1


def test_get_DP_double_param():
    dp = load_data_from_json(
        packed_data={"A": 1.1},
        schema="coek",
    )
    assert dp["A"] == 1.1


def test_get_DP_string_param():
    dp = load_data_from_json(
        packed_data={"A": "a"},
        schema="coek",
    )
    assert dp["A"] == "a"


def test_get_DP_tuple_param():
    dp = load_data_from_json(
        packed_data={"A": ["a", 1, 2.2]},
        schema="coek",
    )
    assert dp["A"] == ("a", 1, 2.2)


#
# Indexed set
#


def test_get_DP_int_set_int():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": "i",
                "set_type": "i",
                "data": [[0, [1]], [1, [1, 2]], [2, [1, 2, 3]]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {0: [1], 1: [1, 2], 2: [1, 2, 3]}


def test_get_DP_int_set_string():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": "i",
                "set_type": "s",
                "data": [[0, ["a"]], [1, ["a", "b"]], [2, ["a", "b", "c"]]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {0: ["a"], 1: ["a", "b"], 2: ["a", "b", "c"]}


def test_get_DP_string_set_string():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": "s",
                "set_type": "s",
                "data": [["A", ["a"]], ["B", ["a", "b"]], ["C", ["a", "b", "c"]]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {"A": ["a"], "B": ["a", "b"], "C": ["a", "b", "c"]}


def test_get_DP_string_set_int():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": "s",
                "set_type": "i",
                "data": [["0", [1]], ["1", [1, 2]], ["2", [1, 2, 3]]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {"0": [1], "1": [1, 2], "2": [1, 2, 3]}


def test_get_DP_stringtuple_set_int():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": ["s", "s"],
                "set_type": "i",
                "data": [
                    [["0", "1"], [1]],
                    [["1", "1"], [1, 2]],
                    [["2", "1"], [1, 2, 3]],
                ],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {("0", "1"): [1], ("1", "1"): [1, 2], ("2", "1"): [1, 2, 3]}


def test_get_DP_inttuple_set_int():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": ["i", "i"],
                "set_type": "i",
                "data": [[[0, 1], [1]], [[1, 1], [1, 2]], [[2, 1], [1, 2, 3]]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {(0, 1): [1], (1, 1): [1, 2], (2, 1): [1, 2, 3]}


def test_get_DP_mixedtuple_set_int():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": ["s", "i"],
                "set_type": "i",
                "data": [[["0", 1], [1]], [["1", 1], [1, 2]], [["2", 1], [1, 2, 3]]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {("0", 1): [1], ("1", 1): [1, 2], ("2", 1): [1, 2, 3]}


def test_get_DP_int_set_inttuple():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": "i",
                "set_type": ["i", "i"],
                "data": [
                    [0, [[1, 1]]],
                    [1, [[1, 1], [2, 2]]],
                    [2, [[1, 1], [2, 2], [3, 3]]],
                ],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {0: [(1, 1)], 1: [(1, 1), (2, 2)], 2: [(1, 1), (2, 2), (3, 3)]}


def test_get_DP_mixedtuple_set_mixedtuple():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": ["s", "i"],
                "set_type": ["i", "s"],
                "data": [
                    [["0", 0], [[1, "1"]]],
                    [["1", 1], [[1, "1"], [2, "2"]]],
                    [["2", 2], [[1, "1"], [2, "2"], [3, "3"]]],
                ],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {
        ("0", 0): [(1, "1")],
        ("1", 1): [(1, "1"), (2, "2")],
        ("2", 2): [(1, "1"), (2, "2"), (3, "3")],
    }


#
# Indexed parameters
#


def test_get_DP_int_int_param():
    dp = load_data_from_json(
        packed_data={"A": {"key_type": "i", "param_type": "i", "data": [[0, 0], [1, 1], [2, 2]]}},
        schema="coek",
    )
    assert dp["A"] == {0: 0, 1: 1, 2: 2}


def test_get_DP_int_string_param():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": "i",
                "param_type": "s",
                "data": [[0, "0"], [1, "1"], [2, "2"]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {0: "0", 1: "1", 2: "2"}


def test_get_DP_string_string_param():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": "s",
                "param_type": "s",
                "data": [["0", "0"], ["1", "1"], ["2", "2"]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {"0": "0", "1": "1", "2": "2"}


def test_get_DP_string_int_param():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": "s",
                "param_type": "i",
                "data": [["0", 0], ["1", 1], ["2", 2]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {"0": 0, "1": 1, "2": 2}


def test_get_DP_stringtuple_int_param():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": ["s", "s"],
                "param_type": "i",
                "data": [[["0", "1"], 0], [["1", "2"], 1], [["2", "3"], 2]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {("0", "1"): 0, ("1", "2"): 1, ("2", "3"): 2}


def test_get_DP_int_tuple_param():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": "i",
                "param_type": ["d", "s", "i"],
                "data": [[1, [0.1, "a", 0]], [2, [1.1, "b", 1]], [3, [2.1, "c", 2]]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {1: (0.1, "a", 0), 2: (1.1, "b", 1), 3: (2.1, "c", 2)}


def test_get_DP_tuple_int_param():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": ["i", "i"],
                "param_type": "i",
                "data": [[[0, 1], 0], [[1, 2], 1], [[2, 3], 2]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {(0, 1): 0, (1, 2): 1, (2, 3): 2}


def test_get_DP_mtuple_int_param():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": ["s", "i"],
                "param_type": "i",
                "data": [[["0", 1], 0], [["1", 2], 1], [["2", 3], 2]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {("0", 1): 0, ("1", 2): 1, ("2", 3): 2}


def test_get_DP_mtuple_double_param():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": ["s", "i"],
                "param_type": "d",
                "data": [[["0", 1], 0.1], [["1", 2], 1.1], [["2", 3], 2.1]],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {("0", 1): 0.1, ("1", 2): 1.1, ("2", 3): 2.1}


def test_get_DP_mtuple_tuple_param():
    dp = load_data_from_json(
        packed_data={
            "A": {
                "key_type": ["s", "i"],
                "param_type": ["d", "s", "i"],
                "data": [
                    [["0", 1], [0.1, "a", 0]],
                    [["1", 2], [1.1, "b", 1]],
                    [["2", 3], [2.1, "c", 2]],
                ],
            }
        },
        schema="coek",
    )
    assert dp["A"] == {
        ("0", 1): (0.1, "a", 0),
        ("1", 2): (1.1, "b", 1),
        ("2", 3): (2.1, "c", 2),
    }


def test_json_string_small():
    json_string = """{
"A": 1
}"""
    dp = load_data_from_json(json_string=json_string)
    assert dp["A"] == 1


def test_json_string_big():
    json_string = """{
"a": 1,
"b": 1.1,
"c": "c",
"d": [1, 1.1, "c"],
"e": { "key_type": "i", "param_type": "i", "data": [[0,0], [1,1], [2,2]] },
"f": { "key_type": ["s","i"], "param_type": ["d","s","i"], "data": [[["0",1], [0.1,"a",0]], [["1",2], [1.1,"b",1]], [["2",3], [2.1,"c",2]]] },
"A": {"set_type": "i", "data": [1, 2, 3]},
"B": {"set_type": "d", "data": [1.1, 2.0, 3.0]},
"C": {"set_type": "s", "data": ["a", "b", "c"]},
"D": {"set_type": ["s", "i", "d"], "data": [["a", 0, 1.0], ["b", 1, 2.2], ["c", 2, 3.3]]},
"E": {"key_type": "i", "set_type": "i", "data": [[0,[1]], [1, [1,2]], [2, [1,2,3]]] },
"F": { "key_type": ["s","i"], "set_type": ["i","s"], "data": [[["0",0],[[1,"1"]]], [["1",1], [[1,"1"],[2,"2"]]], [["2",2], [[1,"1"],[2,"2"],[3,"3"]]]] }
}"""
    dp1 = load_data_from_json(json_string=json_string)
    assert dp1["a"] == 1
    assert dp1["A"] == [1, 2, 3]

    dp2 = JsonDataPortal()
    for name in dp1:
        dp2[name] = dp1[name]

    dp1_str = json.dumps(dp1.data, indent=4, sort_keys=True)
    dp2_str = json.dumps(dp2.data, indent=4, sort_keys=True)
    assert dp1_str == dp2_str
