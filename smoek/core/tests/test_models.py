import pprint
import pytest
from . import models
import smoek as smk
import smoek.pymodel.pyomo


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
