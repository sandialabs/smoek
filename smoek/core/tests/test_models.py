import pprint
import pytest
from . import models
import smoek as smk
import smoek.pymodel.pyomo


def test_small1():
    model = models.small1()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "pow", "x", "2"],
        },
        "constraints": {
            "c": ["==", ["pow", "y", "2"], "4"],
        },
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {},
        "variables": {"x": "x", "y": "y"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["x", "y", "o", "c"]


def test_small2():
    model = models.small2()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "x"],
        },
        "constraints": {
            "c": ["==", ["pow", "y", "2"], "4"],
        },
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {},
        "variables": {"x": "x", "y": "y"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["x", "y", "o", "c"]


def test_small3():
    model = models.small3()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "*", "x", "y"],
        },
        "constraints": {
            "c": ["==", ["pow", "y", "2"], "4"],
        },
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {},
        "variables": {"x": "x", "y": "y"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["x", "y", "o", "c"]


def test_small4():
    model = models.small4()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "pow", "y", "2"],
        },
        "constraints": {
            "c": ["==", ["*", "y", "x"], "4"],
        },
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {},
        "variables": {"x": "x", "y": "y"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["x", "y", "o", "c"]


def test_small5():
    model = models.small5()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "_o": [
                "minimize",
                "+",
                [
                    "/",
                    [
                        "pow",
                        "x",
                        "2",
                    ],
                    "2.0",
                ],
                [
                    "/",
                    [
                        "pow",
                        "x",
                        "2",
                    ],
                    "q",
                ],
            ],
        },
        "constraints": {
            "_c0": [
                "==",
                [
                    "*",
                    [
                        "*",
                        "0.5",
                        "v",
                    ],
                    [
                        "-",
                        "x",
                        "y",
                    ],
                ],
                "2",
            ],
            "_c1": [
                "==",
                [
                    "*",
                    [
                        "/",
                        "v",
                        "2.0",
                    ],
                    [
                        "-",
                        "x",
                        "y",
                    ],
                ],
                "2",
            ],
            "_c10": [
                "==",
                [
                    "*",
                    [
                        "*",
                        "v",
                        [
                            "-",
                            "x",
                            "y",
                        ],
                    ],
                    [
                        "/",
                        "1",
                        "q",
                    ],
                ],
                "2",
            ],
            "_c11": [
                "==",
                [
                    "*",
                    "v",
                    [
                        "-",
                        "x",
                        "y",
                    ],
                ],
                [
                    "*",
                    "2",
                    "q",
                ],
            ],
            "_c2": [
                "==",
                [
                    "/",
                    [
                        "*",
                        "v",
                        [
                            "-",
                            "x",
                            "y",
                        ],
                    ],
                    "2.0",
                ],
                "2",
            ],
            "_c3": [
                "==",
                [
                    "*",
                    "v",
                    [
                        "-",
                        [
                            "/",
                            "x",
                            "2.0",
                        ],
                        [
                            "/",
                            "y",
                            "2.0",
                        ],
                    ],
                ],
                "2",
            ],
            "_c4": [
                "==",
                [
                    "*",
                    [
                        "*",
                        "v",
                        [
                            "-",
                            "x",
                            "y",
                        ],
                    ],
                    "0.5",
                ],
                "2",
            ],
            "_c5": [
                "==",
                [
                    "*",
                    "v",
                    [
                        "-",
                        "x",
                        "y",
                    ],
                ],
                "4.0",
            ],
            "_c6": [
                "==",
                [
                    "*",
                    [
                        "*",
                        [
                            "/",
                            "1",
                            "q",
                        ],
                        "v",
                    ],
                    [
                        "-",
                        "x",
                        "y",
                    ],
                ],
                "2",
            ],
            "_c7": [
                "==",
                [
                    "*",
                    [
                        "/",
                        "v",
                        "q",
                    ],
                    [
                        "-",
                        "x",
                        "y",
                    ],
                ],
                "2",
            ],
            "_c8": [
                "==",
                [
                    "/",
                    [
                        "*",
                        "v",
                        [
                            "-",
                            "x",
                            "y",
                        ],
                    ],
                    "q",
                ],
                "2",
            ],
            "_c9": [
                "==",
                [
                    "*",
                    "v",
                    [
                        "-",
                        [
                            "/",
                            "x",
                            "2.0",
                        ],
                        [
                            "/",
                            "y",
                            "q",
                        ],
                    ],
                ],
                "2",
            ],
        },
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {"q": "q"},
        "variables": {"x": "x", "y": "y", "v": "v"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == [
        "x",
        "y",
        "v",
        "q",
        "_o",
        "_c0",
        "_c1",
        "_c2",
        "_c3",
        "_c4",
        "_c5",
        "_c6",
        "_c7",
        "_c8",
        "_c9",
        "_c10",
        "_c11",
    ]


def test_small6():
    model = models.small6()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "_o": ["minimize", "_v0"],
        },
        "constraints": {
            "_c0": [
                "==",
                [
                    "*",
                    [
                        "*",
                        [
                            "/",
                            "1",
                            "_v3",
                        ],
                        "_v2",
                    ],
                    [
                        "-",
                        "_v0",
                        "_v1",
                    ],
                ],
                "2",
            ],
            "_c1": [
                "==",
                [
                    "*",
                    [
                        "/",
                        "_v2",
                        "_v3",
                    ],
                    [
                        "-",
                        "_v0",
                        "_v1",
                    ],
                ],
                "2",
            ],
            "_c2": [
                "==",
                [
                    "/",
                    [
                        "*",
                        "_v2",
                        [
                            "-",
                            "_v0",
                            "_v1",
                        ],
                    ],
                    "_v3",
                ],
                "2",
            ],
            "_c3": [
                "==",
                [
                    "*",
                    "_v2",
                    [
                        "-",
                        [
                            "/",
                            "_v0",
                            "_v3",
                        ],
                        [
                            "/",
                            "_v1",
                            "_v3",
                        ],
                    ],
                ],
                "2",
            ],
            "_c4": [
                "==",
                [
                    "*",
                    [
                        "*",
                        "_v2",
                        [
                            "-",
                            "_v0",
                            "_v1",
                        ],
                    ],
                    [
                        "/",
                        "1",
                        "_v3",
                    ],
                ],
                "2",
            ],
            "_c5": [
                "==",
                [
                    "*",
                    "_v2",
                    [
                        "-",
                        "_v0",
                        "_v1",
                    ],
                ],
                [
                    "*",
                    "2",
                    "_v3",
                ],
            ],
        },
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {},
        "variables": {"_v0": "_v0", "_v1": "_v1", "_v2": "_v2", "_v3": "_v3"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == [
        "_v0",
        "_v1",
        "_v2",
        "_v3",
        "_o",
        "_c0",
        "_c1",
        "_c2",
        "_c3",
        "_c4",
        "_c5",
    ]


def test_testing1():
    model = models.testing1()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "_o": ["maximize", "+", ["*", "3", "a"], "q"],
        },
        "constraints": {
            "_c0": [
                "<=",
                [
                    "-",
                    [
                        "+",
                        [
                            "*",
                            "3",
                            "b",
                        ],
                        "q",
                    ],
                    "a",
                ],
                "0",
            ],
            "_c1": [
                "==",
                [
                    "+",
                    [
                        "*",
                        "3",
                        "b",
                    ],
                    "b",
                ],
                "0",
            ],
            "_c2": [
                "==",
                [
                    "+",
                    [
                        "+",
                        [
                            "+",
                            [
                                "*",
                                [
                                    "*",
                                    "3",
                                    "b",
                                ],
                                "a",
                            ],
                            "q",
                        ],
                        [
                            "*",
                            "b",
                            "b",
                        ],
                    ],
                    [
                        "*",
                        "b",
                        "b",
                    ],
                ],
                "0",
            ],
            "_c3": [
                "<=",
                [
                    "-",
                    [
                        "-",
                        [
                            "+",
                            [
                                "*",
                                [
                                    "*",
                                    "3",
                                    "b",
                                ],
                                "b",
                            ],
                            "q",
                        ],
                        [
                            "*",
                            "a",
                            "b",
                        ],
                    ],
                    [
                        "*",
                        "a",
                        "a",
                    ],
                ],
                "0",
            ],
            "_c4": [
                '<=',
                '-7',
                [
                    '-',
                    [
                        '-',
                        [
                            '+',
                            [
                                '*',
                                [
                                    '*',
                                    '3',
                                    'b',
                                ],
                                'b',
                            ],
                            'q',
                        ],
                        [
                            '*',
                            'a',
                            'b',
                        ],
                    ],
                    [
                        '*',
                        'a',
                        'a',
                    ],
                ],
                '7',
            ],
            "_c5": [
                "==",
                [
                    "+",
                    "_v2",
                    "_v3",
                ],
                "0",
            ],
            "_c6": [
                "==",
                [
                    "+",
                    "e",
                    [
                        "*",
                        "3",
                        "_v3",
                    ],
                ],
                "1",
            ],
            "_c7": [
                '<=',
                '7',
                [
                    '-',
                    [
                        '+',
                        [
                            '*',
                            '3',
                            'b',
                        ],
                        'q',
                    ],
                    'a',
                ],
                '7',
            ],
        },
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {"q": "q"},
        "variables": {"a": "a", "b": "b", "e": "e", "_v2": "_v2", "_v3": "_v3"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == [
        "a",
        "b",
        "_v2",
        "_v3",
        "e",
        "q",
        "_o",
        "_c0",
        "_c1",
        "_c2",
        "_c3",
        "_c4",
        "_c5",
        "_c6",
        "_c7",
    ]


def test_testing2():
    model = models.testing2()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "_o": [
                "minimize",
                "+",
                [
                    "+",
                    [
                        "+",
                        [
                            "*",
                            "3",
                            "a",
                        ],
                        "q",
                    ],
                    [
                        "*",
                        [
                            "*",
                            [
                                "*",
                                "a",
                                "a",
                            ],
                            "a",
                        ],
                        [
                            "+",
                            [
                                "+",
                                [
                                    "+",
                                    [
                                        "neg",
                                        "a",
                                    ],
                                    "b",
                                ],
                                [
                                    "*",
                                    "3",
                                    "a",
                                ],
                            ],
                            [
                                "*",
                                "3",
                                "b",
                            ],
                        ],
                    ],
                ],
                [
                    "sin",
                    [
                        "neg",
                        [
                            "cos",
                            "a",
                        ],
                    ],
                ],
            ],
        },
        "constraints": {},
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {"q": "q"},
        "variables": {"a": "a", "b": "b"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["a", "b", "q", "_o"]


# TODO - Add smk.expression()
def Xtest_testing3():
    model = models.testing3()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "e"],
        },
        "constraints": {
            "_c0": ["==", ["+", "a", "b"], "1"],
        },
        "data": {},
        "expressions": {"_e0": 0},
        "index_sets": {},
        "parameters": {},
        "variables": {"a": "a", "b": "b"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["a", "b", "_o", "_c0"]


def test_testing4():
    model = models.testing4()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "_o": ["minimize", "+", ["+", "a", ["cos", "x"]], ["cos", "y"]],
        },
        "constraints": {
            "_c0": ["==", ["+", ["+", "b", ["cos", "y"]], ["cos", "z"]], "1"],
        },
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {},
        "variables": {"a": "a", "b": "b", "x": "x", "y": "y", "z": "z"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["x", "y", "z", "a", "b", "_o", "_c0"]


def test_testing5():
    model = models.testing5()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "x"],
        },
        "constraints": {},
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {},
        "variables": {"x": "x"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["x", "o"]


def test_testing6():
    model = models.testing6()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": [
                "minimize",
                "+",
                [
                    "*",
                    [
                        "*",
                        [
                            "neg",
                            "q",
                        ],
                        "x",
                    ],
                    "x",
                ],
                "p",
            ],
        },
        "constraints": {},
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {"p": "p", "q": "q"},
        "variables": {"x": "x"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["x", "p", "q", "o"]


def test_testing7():
    model = models.testing7()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "*", "p", "x"],
        },
        "constraints": {
            "c": [
                "==",
                "x",
                "0",
            ],
            "cc": [
                "==",
                [
                    "*",
                    "pp[i]",
                    "xx[i]",
                ],
                "0",
            ],
            "ccc": [
                "==",
                [
                    "*",
                    "ppp[i, j]",
                    "xxx[i, j]",
                ],
                "0",
            ],
        },
        "data": {},
        "expressions": {},
        "index_sets": {"A": "range(stop=10)", "B": "range(stop=11)"},
        "parameters": {
            "p": "p",
            "pp": "pp, forall i in A",
            "ppp": "ppp, forall i in A, i in B",
        },
        "variables": {
            "x": "x",
            "xx": "xx, forall i in A",
            "xxx": "xxx, forall i in A, i in B",
        },
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == [
        "A",
        "B",
        "i",
        "j",
        "p",
        "pp",
        "ppp",
        "x",
        "xx",
        "xxx",
        "o",
        "c",
        "cc",
        "ccc",
    ]


def test_simple1():
    model = models.simple1()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "+", "x", "y"],
        },
        "constraints": {
            "c1": ["==", ["+", "x", "y"], "1"],
            "c2": ["<=", ["+", ["*", "2", "x"], "y"], "1"],
            "c3": [">=", ["-", "y", ["*", "2", "x"]], "1"],
        },
        "data": {},
        "expressions": {},
        "index_sets": {},
        "parameters": {},
        "variables": {"x": "x", "y": "y"},
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["x", "y", "o", "c1", "c2", "c3"]


def test_hs060():
    model = models.hs060()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": [
                "minimize",
                "+",
                [
                    "+",
                    ["pow", ["-", "x[1]", "1"], "2"],
                    ["pow", ["-", "x[1]", "x[2]"], "2"],
                ],
                ["pow", ["-", "x[2]", "x[3]"], "4"],
            ],
        },
        "constraints": {
            "c": [
                "==",
                [
                    "+",
                    ["*", "x[1]", ["+", "1", ["pow", "x[2]", "2"]]],
                    ["pow", "x[3]", "4"],
                ],
                ["+", "4", ["*", "3", ["sqrt", "2"]]],
            ],
        },
        "data": {},
        "expressions": {},
        "index_sets": {"N": "sequence(start=1, stop=4)"},
        "parameters": {},
        "variables": {
            "x": "x, forall i in N",
        },
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["N", "x", "o", "c"]


def test_knapsack1():
    model = models.knapsack1(1)

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "sum", "forall i in INDEX", ["*", "v[i]", "x[i]"]],
        },
        "constraints": {
            "c": ["<=", ["sum", "forall i in INDEX", ["*", "w[i]", "x[i]"]], "1.0"],
        },
        "data": {},
        "expressions": {},
        "index_sets": {
            "INDEX": "range(stop=10)",
        },
        "parameters": {
            "v": "v, forall i in INDEX",
            "w": "w, forall i in INDEX",
        },
        "variables": {
            "x": "x, forall i in INDEX",
        },
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["i", "INDEX", "w", "v", "x", "o", "c"]


def test_knapsack2():
    model = models.knapsack2(1)

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "sum", "forall i in INDEX", ["*", "v[i]", "x[i]"]],
        },
        "constraints": {
            "c": [
                "<=",
                ["sum", "forall i in INDEX", ["*", "w[i]", "x[i]"]],
                ["/", ["*", "N", "10"], "10.0"],
            ],
        },
        "data": {},
        "expressions": {},
        "index_sets": {
            "INDEX": "range(stop=N * 10)",
        },
        "parameters": {
            "N": "N",
            "v": "v, forall i in INDEX",
            "w": "w, forall i in INDEX",
        },
        "variables": {
            "x": "x, forall i in INDEX",
        },
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["N", "i", "INDEX", "w", "v", "x", "o", "c"]


def test_knapsack3():
    model = models.knapsack3()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "sum", "forall i in INDEX", ["*", "v[i]", "x[i]"]],
        },
        "constraints": {
            "c": [
                "<=",
                ["sum", "forall i in INDEX", ["*", "w[i]", "x[i]"]],
                ["/", ["*", "N", "10"], "10.0"],
            ],
        },
        "data": {},
        "expressions": {},
        "index_sets": {
            "INDEX": "range(stop=N * 10)",
        },
        "parameters": {
            "N": "N",
            "v": "v, forall i in INDEX",
            "w": "w, forall i in INDEX",
        },
        "variables": {
            "x": "x, forall i in INDEX",
        },
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["N", "i", "INDEX", "w", "v", "x", "o", "c"]


def test_knapsack4():
    model = models.knapsack4()

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "sum", "forall i in ITEMS", ["*", "value[i]", "x[i]"]],
        },
        "constraints": {
            "c": [
                "<=",
                ["sum", "forall i in ITEMS", ["*", "weight[i]", "x[i]"]],
                "capacity"
            ],
        },
        "data": {},
        "expressions": {},
        "index_sets": {
            "ITEMS": "ITEMS",
        },
        "parameters": {
            "capacity": "capacity",
            "value": "value, forall i in ITEMS",
            "weight": "weight, forall i in ITEMS",
        },
        "variables": {
            "x": "x, forall i in ITEMS",
        },
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["ITEMS", "i", "value", "weight", "capacity", "x", "o", "c"]
