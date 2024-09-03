import pytest
import smoek as smk
from smoek.core.tests import models
from smoek.code.pyomo import generate


def test_small1():
    model = models.small1()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_small1(data):
    M = pyo.ConcreteModel("small1")

    M.x = pyo.Var(initialize=1.0)

    M.y = pyo.Var(initialize=1.0)

    M.o = pyo.Objective(expr=pow(M.x, 2))

    M.c = pyo.Constraint(expr=pow(M.y, 2) == 4)

    return M
"""
    )


def test_small2():
    model = models.small2()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_small2(data):
    M = pyo.ConcreteModel("small2")

    M.x = pyo.Var(initialize=1.0)

    M.y = pyo.Var(initialize=1.0)

    M.o = pyo.Objective(expr=M.x)

    M.c = pyo.Constraint(expr=pow(M.y, 2) == 4)

    return M
"""
    )


def test_small3():
    model = models.small3()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_small3(data):
    M = pyo.ConcreteModel("small3")

    M.x = pyo.Var(initialize=1.0)

    M.y = pyo.Var(initialize=1.0)

    M.o = pyo.Objective(expr=M.x * M.y)

    M.c = pyo.Constraint(expr=pow(M.y, 2) == 4)

    return M
"""
    )


def test_small4():
    model = models.small4()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_small4(data):
    M = pyo.ConcreteModel("small4")

    M.x = pyo.Var(initialize=1.0)

    M.y = pyo.Var(initialize=1.0)

    M.o = pyo.Objective(expr=pow(M.y, 2))

    M.c = pyo.Constraint(expr=M.y * M.x == 4)

    return M
"""
    )


def test_small5():
    model = models.small5()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_small5(data):
    M = pyo.ConcreteModel("small5")

    M.x = pyo.Var(bounds=(-1,1), initialize=1.0)

    M.y = pyo.Var(bounds=(-1,1), initialize=2.0)

    M.v = pyo.Var(bounds=(-1,1), initialize=3.0)

    M.q = pyo.Param(mutable=True, initialize=2)

    M._o = pyo.Objective(expr=(pow(M.x, 2) / 2.0) + (pow(M.x, 2) / M.q))

    M._c0 = pyo.Constraint(expr=(0.5 * M.v) * (M.x - M.y) == 2)

    M._c1 = pyo.Constraint(expr=(M.v / 2.0) * (M.x - M.y) == 2)

    M._c2 = pyo.Constraint(expr=(M.v * (M.x - M.y)) / 2.0 == 2)

    M._c3 = pyo.Constraint(expr=M.v * ((M.x / 2.0) - (M.y / 2.0)) == 2)

    M._c4 = pyo.Constraint(expr=(M.v * (M.x - M.y)) * 0.5 == 2)

    M._c5 = pyo.Constraint(expr=M.v * (M.x - M.y) == 4.0)

    M._c6 = pyo.Constraint(expr=((1 / M.q) * M.v) * (M.x - M.y) == 2)

    M._c7 = pyo.Constraint(expr=(M.v / M.q) * (M.x - M.y) == 2)

    M._c8 = pyo.Constraint(expr=(M.v * (M.x - M.y)) / M.q == 2)

    M._c9 = pyo.Constraint(expr=M.v * ((M.x / 2.0) - (M.y / M.q)) == 2)

    M._c10 = pyo.Constraint(expr=(M.v * (M.x - M.y)) * (1 / M.q) == 2)

    M._c11 = pyo.Constraint(expr=M.v * (M.x - M.y) == 2 * M.q)

    return M
"""
    )


def test_small6():
    model = models.small6()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_small6(data):
    M = pyo.ConcreteModel("small6")

    M._v0 = pyo.Var(bounds=(-1,1), initialize=1)

    M._v1 = pyo.Var(bounds=(-1,1), initialize=2)

    M._v2 = pyo.Var(bounds=(-1,1), initialize=3)

    M._v3 = pyo.Var(initialize=2)
    M._v3.fix()

    M._o = pyo.Objective(expr=M._v0)

    M._c0 = pyo.Constraint(expr=((1 / M._v3) * M._v2) * (M._v0 - M._v1) == 2)

    M._c1 = pyo.Constraint(expr=(M._v2 / M._v3) * (M._v0 - M._v1) == 2)

    M._c2 = pyo.Constraint(expr=(M._v2 * (M._v0 - M._v1)) / M._v3 == 2)

    M._c3 = pyo.Constraint(expr=M._v2 * ((M._v0 / M._v3) - (M._v1 / M._v3)) == 2)

    M._c4 = pyo.Constraint(expr=(M._v2 * (M._v0 - M._v1)) * (1 / M._v3) == 2)

    M._c5 = pyo.Constraint(expr=M._v2 * (M._v0 - M._v1) == 2 * M._v3)

    return M
"""
    )


def test_testing1():
    model = models.testing1()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing1(data):
    M = pyo.ConcreteModel("testing1")

    M.a = pyo.Var(bounds=(0,1), initialize=0)

    M.b = pyo.Var(bounds=(0,1), initialize=0)

    M._v2 = pyo.Var(bounds=(0,None))

    M._v3 = pyo.Var(bounds=(None,0))

    M.e = pyo.Var()
    M.e.fix()

    M.q = pyo.Param(mutable=True, initialize=2)

    M._o = pyo.Objective(expr=(3 * M.a) + M.q)

    M._c0 = pyo.Constraint(expr=((3 * M.b) + M.q) - M.a <= 0)

    M._c1 = pyo.Constraint(expr=(3 * M.b) + M.b == 0)

    M._c2 = pyo.Constraint(expr=((((3 * M.b) * M.a) + M.q) + (M.b * M.b)) + (M.b * M.b) == 0)

    M._c3 = pyo.Constraint(expr=((((3 * M.b) * M.b) + M.q) - (M.a * M.b)) - (M.a * M.a) <= 0)

    M._c4 = pyo.Constraint(expr=((((3 * M.b) * M.b) + M.q) - (M.a * M.b)) - (M.a * M.a) <= 7 >= -7)

    M._c5 = pyo.Constraint(expr=M._v2 + M._v3 == 0)

    M._c6 = pyo.Constraint(expr=M.e + (3 * M._v3) == 1)

    M._c7 = pyo.Constraint(expr=((3 * M.b) + M.q) - M.a <= 7 >= 7)

    return M
"""
    )


def test_testing2():
    model = models.testing2()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing2(data):
    M = pyo.ConcreteModel("testing2")

    M.a = pyo.Var(bounds=(0,1), initialize=0)

    M.b = pyo.Var(bounds=(0,1), initialize=0)

    M.q = pyo.Param(mutable=True, initialize=2)

    M._o = pyo.Objective(expr=(((3 * M.a) + M.q) + (((M.a * M.a) * M.a) * (((pyo.neg(M.a) + M.b) + (3 * M.a)) + (3 * M.b)))) + pyo.sin(pyo.neg(pyo.cos(M.a))))

    return M
"""
    )


# TODO: smk.expression()
def Xtest_testing3():
    model = models.testing3()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing3(data):
    M = pyo.ConcreteModel("testing3")

    return M
"""
    )


def test_testing4():
    model = models.testing4()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing4(data):
    M = pyo.ConcreteModel("testing4")

    M.x = pyo.Var(bounds=(0,1), initialize=0)

    M.y = pyo.Var(bounds=(0,1), initialize=0)

    M.z = pyo.Var(bounds=(0,1), initialize=0)

    M.a = pyo.Var(bounds=(0,1), initialize=0)

    M.b = pyo.Var(bounds=(0,1), initialize=0)

    M._o = pyo.Objective(expr=(M.a + pyo.cos(M.x)) + pyo.cos(M.y))

    M._c0 = pyo.Constraint(expr=(M.b + pyo.cos(M.y)) + pyo.cos(M.z) == 1)

    return M
"""
    )


def test_testing5():
    model = models.testing5()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing5(data):
    M = pyo.ConcreteModel("testing5")

    M.x = pyo.Var(bounds=(2,2), initialize=0)

    M.o = pyo.Objective(expr=M.x)

    return M
"""
    )


def test_testing6():
    model = models.testing6()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing6(data):
    M = pyo.ConcreteModel("testing6")

    M.x = pyo.Var(bounds=(0,1), initialize=0)

    M.p = pyo.Param(mutable=True)

    M.q = pyo.Param(mutable=True, initialize=2)

    M.o = pyo.Objective(expr=((pyo.neg(M.q) * M.x) * M.x) + M.p)

    return M
"""
    )


def test_testing7():
    model = models.testing7()

    assert (
        generate(model=model)
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing7(data):
    M = pyo.ConcreteModel("testing7")

    M.A = pyo.RangeSet(0, 10)

    M.B = pyo.RangeSet(0, 11)

    M.p = pyo.Param(mutable=True)

    M.pp = pyo.Param(M.A, mutable=True)

    M.ppp = pyo.Param(M.A, M.B, mutable=True)

    M.x = pyo.Var()

    M.xx = pyo.Var(M.A)

    M.xxx = pyo.Var(M.A, M.B)

    M.o = pyo.Objective(expr=M.p * M.x)

    M.c = pyo.Constraint(expr=M.x == 0)

    def cc_(m,i):
        return m.pp[i] * m.xx[i] == 0
    M.cc = pyo.Constraint(M.A, rule=cc_)

    def ccc_(m,i,j):
        return m.ppp[i,j] * m.xxx[i,j] == 0
    M.ccc = pyo.Constraint(M.A, M.B, rule=ccc_)

    return M
"""
    )


def test_simple1():
    model = models.simple1()

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

    # print(generate(model=model))
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

    # print(generate(model=model))
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

    # print(generate(model=model, data={"N": "int"}))
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


def test_knapsack4():
    model = models.knapsack4()

    # print(generate(model=model, data={"N": "int"}))
    assert (
        generate(model=model, data={"ITEMS": "int", "max_weight":"unsigned int", "value":"double", "weight":"unsigned int"})
        == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_knapsack4(data):
    M = pyo.ConcreteModel("knapsack4")

    M.ITEMS = pyo.Set()

    M.value = pyo.Param(M.ITEMS, mutable=True, initialize=data["value"])

    M.weight = pyo.Param(M.ITEMS, mutable=True, initialize=data["weight"])

    M.max_weight = pyo.Param(mutable=True, initialize=data["max_weight"])

    M.x = pyo.Var(M.ITEMS, bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=sum(M.value[i] * M.x[i] for i in M.ITEMS))

    M.c = pyo.Constraint(expr=sum(M.weight[i] * M.x[i] for i in M.ITEMS) <= M.max_weight)

    return M
"""
    )
