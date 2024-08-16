import pytest
import smoek as smk
from smoek.core.tests import models
from smoek.code.pyomo import generate


def test_simple1():
    model = models.simple1()

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["x", "y", "o", "c1", "c2", "c3"]

    # print(generate(model=model))
    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_simple1(data):
    M = pyo.ConcreteModel("simple1")

    M.x = pyo.Var(bounds=(0.0,1.0))

    M.y = pyo.Var(bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=M.x + M.y)

    M.c1 = pyo.Constraint(expr=M.x + M.y == 1)

    M.c2 = pyo.Constraint(expr=(2 * M.x) + M.y <= 1)

    M.c3 = pyo.Constraint(expr=M.y - (2 * M.x) >= 1)

    return M
"""
    )


def test_hs060():
    model = models.hs060()

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["N", "x", "o", "c"]

    # print(generate(model=model))
    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_hs060(data):
    M = pyo.ConcreteModel("hs060")

    M.N = pyo.RangeSet(1, 4+1)

    M.x = pyo.Var(M.N, bounds=(-10,10), initialize=2.0)

    M.o = pyo.Objective(expr=(pow(M.x[1] - 1, 2) + pow(M.x[1] - M.x[2], 2)) + pow(M.x[2] - M.x[3], 4))

    M.c = pyo.Constraint(expr=(M.x[1] * (1 + pow(M.x[2], 2))) + pow(M.x[3], 4) == 4 + (3 * pyo.sqrt(2)))

    return M
"""
    )


def test_knapsack1():
    model = models.knapsack1(1)

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["i", "INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model))
    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_knapsack1(data):
    M = pyo.ConcreteModel("knapsack1")

    M.INDEX = pyo.RangeSet(0, 10)

    M.w = pyo.Param(M.INDEX, mutable=True, initialize=1.0)

    M.v = pyo.Param(M.INDEX, mutable=True, initialize=1)

    M.x = pyo.Var(M.INDEX, bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=sum(M.v[i] * M.x[i] for i in M.INDEX))

    M.c = pyo.Constraint(expr=sum(M.w[i] * M.x[i] for i in M.INDEX) <= 1.0)

    return M
"""
    )

def test_knapsack2():
    model = models.knapsack2(1)

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["N", "i", "INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model))
    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_knapsack2(data):
    M = pyo.ConcreteModel("knapsack2")

    M.N = pyo.Param(mutable=True, initialize=1)

    M.INDEX = pyo.RangeSet(0, M.N * 10)

    M.w = pyo.Param(M.INDEX, mutable=True, initialize=1 / ((M.N * 10) / 10.0))

    M.v = pyo.Param(M.INDEX, mutable=True, initialize=1)

    M.x = pyo.Var(M.INDEX, bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=sum(M.v[i] * M.x[i] for i in M.INDEX))

    M.c = pyo.Constraint(expr=sum(M.w[i] * M.x[i] for i in M.INDEX) <= (M.N * 10) / 10.0)

    return M
"""
    )


def test_knapsack3():
    model = models.knapsack3()

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["N", "i", "INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model, data={"N": "int"}))
    assert (
        generate(model=model, data={"N": "int"})
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_knapsack3(data):
    M = pyo.ConcreteModel("knapsack3")

    M.N = pyo.Param(mutable=True, initialize=data["N"])

    M.INDEX = pyo.RangeSet(0, M.N * 10)

    M.w = pyo.Param(M.INDEX, mutable=True, initialize=1 / ((M.N * 10) / 10.0))

    M.v = pyo.Param(M.INDEX, mutable=True, initialize=1)

    M.x = pyo.Var(M.INDEX, bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=sum(M.v[i] * M.x[i] for i in M.INDEX))

    M.c = pyo.Constraint(expr=sum(M.w[i] * M.x[i] for i in M.INDEX) <= (M.N * 10) / 10.0)

    return M
"""
    )
