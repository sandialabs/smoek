import pprint
import pytest
from . import models
import smoek as smk
import smoek.pymodel.pyomo


def test_simple1():
    model = models.simple1()

    repn = smk.model_to_dict(model)
    assert repn == {
        "o": ["minimize", "+", "x", "y"],
        "c1": ["==", ["+", "x", "y"], "1"],
        "c2": ["<=", ["+", ["*", "2", "x"], "y"], "1"],
        "c3": [">=", ["-", "y", ["*", "2", "x"]], "1"],
    }


def test_hs060():
    model = models.hs060()

    repn = smk.model_to_dict(model)
    assert repn == {
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
        "c": [
            "==",
            [
                "+",
                ["*", "x[1]", ["+", "1", ["pow", "x[2]", "2"]]],
                ["pow", "x[3]", "4"],
            ],
            ["+", "4", ["*", "3", ["sqrt", "2"]]],
        ],
    }


def test_knapsack1():
    model = models.knapsack1(10)

    repn = smk.model_to_dict(model)
    assert repn == {
        "o": ["minimize", "sum", "forall i in INDEX", ["*", "v[i]", "x[i]"]],
        "c": ["<=", ["sum", "forall i in INDEX", ["*", "w[i]", "x[i]"]], "1000.0"],
    }
