import pytest
import smoek as smk
from smoek.core.tests import models
from smoek.code.coek import generate


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

    #print(generate(model=model))
    assert generate(model=model) == """
#include <coek/coek.hpp>

coek::Model generate_simple1()
{
coek::Model model("simple1");

auto x = coek::variable(x).lower(0.0).upper(1.0);
model.add(x);

auto y = coek::variable(y).lower(0.0).upper(1.0);
model.add(y);

auto o = coek::objective(o).expr(x + y);
model.add(o);

auto c1 = coek::constraint(c1).expr(x + y == 1);
model.add(c1);

auto c2 = coek::constraint(c2).expr((2 * x) + y <= 1);
model.add(c2);

auto c3 = coek::constraint(c3).expr(y - (2 * x) >= 1);
model.add(c3);

return model;
}
"""


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
            "x": "x, forall UnnamedComponent in N",
        },
    }

    order = smk.valid_order(smk.collect_info(model))
    assert order == ["N", "x", "o", "c"]

    #print(generate(model=model))
    assert generate(model=model) == """
#include <coek/coek.hpp>

coek::Model generate_hs060()
{
coek::Model model("hs060");

coek::RangeSet N(1, 4+1);

auto x = coek::variable(x, N).lower(-10).upper(10).value(2.0);
model.add(x);

auto o = coek::objective(o).expr((coek::pow(x[1] - 1, 2) + coek::pow(x[1] - x[2], 2)) + coek::pow(x[2] - x[3], 4));
model.add(o);

auto c = coek::constraint(c).expr((x[1] * (1 + coek::pow(x[2], 2))) + coek::pow(x[3], 4) == 4 + (3 * coek::sqrt(2)));
model.add(c);

return model;
}
"""


def test_knapsack1():
    model = models.knapsack1(10)

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "sum", "forall i in INDEX", ["*", "v[i]", "x[i]"]],
        },
        "constraints": {
            "c": ["<=", ["sum", "forall i in INDEX", ["*", "w[i]", "x[i]"]], "1000.0"],
        },
        "data": {},
        "expressions": {},
        "index_sets": {
            "INDEX": "range(stop=10000)",
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
    assert order == ["INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model))
    assert generate(model=model) == ""

def test_knapsack2():
    model = models.knapsack2(10)

    repn = smk.model_to_dict(model)
    assert repn == {
        "objectives": {
            "o": ["minimize", "sum", "forall i in INDEX", ["*", "v[i]", "x[i]"]],
        },
        "constraints": {
            "c": [
                "<=",
                ["sum", "forall i in INDEX", ["*", "w[i]", "x[i]"]],
                ["/", ["*", "N", "1000"], "10.0"],
            ],
        },
        "data": {},
        "expressions": {},
        "index_sets": {
            "INDEX": "range(stop=N * 1000)",
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
    assert order == ["N", "INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model))
    assert generate(model=model) == ""
