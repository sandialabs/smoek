import pytest
import smoek as smk
from smoek.core.tests import models
from smoek.code.coek import generate


def test_simple1():
    model = models.simple1()

    #order = smk.valid_order(smk.collect_info(model))
    #assert order == ["x", "y", "o", "c1", "c2", "c3"]

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

    #order = smk.valid_order(smk.collect_info(model))
    #assert order == ["N", "x", "o", "c"]

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

    #order = smk.valid_order(smk.collect_info(model))
    #assert order == ["INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model))
    assert generate(model=model) == """
#include <coek/coek.hpp>

coek::Model generate_knapsack1()
{
coek::Model model("knapsack1");

coek::RangeSet INDEX(10000);

auto w = coek::parameter(w, INDEX).value(0.001);

auto v = coek::parameter(v, INDEX).value(1);

auto x = coek::variable(x, INDEX).lower(0.0).upper(1.0);
model.add(x);

auto o = coek::objective(o).expr(coek::Sum(v[i] * x[i], Forall(i).In(INDEX)));
model.add(o);

auto c = coek::constraint(c).expr(coek::Sum(w[i] * x[i], Forall(i).In(INDEX)) <= 1000.0);
model.add(c);

return model;
}
"""

def test_knapsack2():
    model = models.knapsack2(10)

    #order = smk.valid_order(smk.collect_info(model))
    #assert order == ["N", "INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model))
    assert generate(model=model) == """
#include <coek/coek.hpp>

coek::Model generate_knapsack2()
{
coek::Model model("knapsack2");

auto N = coek::parameter(N).value(10).value(10);

coek::RangeSet INDEX(N * 1000);

auto w = coek::parameter(w, INDEX).value(1 / ((N * 1000) / 10.0));

auto v = coek::parameter(v, INDEX).value(1);

auto x = coek::variable(x, INDEX).lower(0.0).upper(1.0);
model.add(x);

auto o = coek::objective(o).expr(coek::Sum(v[i] * x[i], Forall(i).In(INDEX)));
model.add(o);

auto c = coek::constraint(c).expr(coek::Sum(w[i] * x[i], Forall(i).In(INDEX)) <= (N * 1000) / 10.0);
model.add(c);

return model;
}
"""
