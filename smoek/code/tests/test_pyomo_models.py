import pytest
import smoek as smk
from smoek.core.tests import models
from smoek.code.pyomo import generate


def test_small1():
    model = models.small1()

    assert generate(model=model) == """
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


def test_small2():
    model = models.small2()

    assert generate(model=model) == """
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


def test_small3():
    model = models.small3()

    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_small3(data):
    M = pyo.ConcreteModel("small3")

    M.x = pyo.Var(initialize=1.0)

    M.y = pyo.Var(initialize=1.0)

    M.o = pyo.Objective(expr=(-(M.x * M.y)))

    M.c = pyo.Constraint(expr=pow(M.y, 2) == 4)

    return M
"""


def test_small4():
    model = models.small4()

    assert generate(model=model) == """
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


def test_small5():
    model = models.small5()

    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_small5(data):
    M = pyo.ConcreteModel("small5")

    M.x = pyo.Var(bounds=(-1,1), initialize=1.0)

    M.y = pyo.Var(bounds=(-1,2), initialize=2.0)

    M.v = pyo.Var(bounds=(-1,3), initialize=3.0)

    M.q = pyo.Param(mutable=True, initialize=2, within=pyo.Reals)

    M.o = pyo.Objective(expr=(pow(M.x, 2) / 2.0) + (pow(M.x, 2) / M.q))

    M.c_0_ = pyo.Constraint(expr=(0.5 * M.v) * (M.x - M.y) == 2)

    M.c_1_ = pyo.Constraint(expr=(M.v / 2.0) * (M.x - M.y) == 2)

    M.c_2_ = pyo.Constraint(expr=(M.v * (M.x - M.y)) / 2.0 == 2)

    M.c_3_ = pyo.Constraint(expr=M.v * ((M.x / 2.0) - (M.y / 2.0)) == 2)

    M.c_4_ = pyo.Constraint(expr=(M.v * (M.x - M.y)) * 0.5 == 2)

    M.c_5_ = pyo.Constraint(expr=M.v * (M.x - M.y) == 4.0)

    M.c_6_ = pyo.Constraint(expr=((1 / M.q) * M.v) * (M.x - M.y) == 2)

    M.c_7_ = pyo.Constraint(expr=(M.v / M.q) * (M.x - M.y) == 2)

    M.c_8_ = pyo.Constraint(expr=(M.v * (M.x - M.y)) / M.q == 2)

    M.c_9_ = pyo.Constraint(expr=M.v * ((M.x / 2.0) - (M.y / M.q)) == 2)

    M.c_10_ = pyo.Constraint(expr=(M.v * (M.x - M.y)) * (1 / M.q) == 2)

    M.c_11_ = pyo.Constraint(expr=M.v * (M.x - M.y) == 2 * M.q)

    return M
"""


def test_small6():
    model = models.small6()

    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_small6(data):
    M = pyo.ConcreteModel("small6")

    M.x = pyo.Var(bounds=(-1,1), initialize=1)

    M.y = pyo.Var(bounds=(-1,2), initialize=2)

    M.v = pyo.Var(bounds=(-1,3), initialize=3)

    M.p = pyo.Var(initialize=2)
    M.p.fix()

    M.o = pyo.Objective(expr=M.x)

    M.c_0_ = pyo.Constraint(expr=((1 / M.p) * M.v) * (M.x - M.y) == 2)

    M.c_1_ = pyo.Constraint(expr=(M.v / M.p) * (M.x - M.y) == 2)

    M.c_2_ = pyo.Constraint(expr=(M.v * (M.x - M.y)) / M.p == 2)

    M.c_3_ = pyo.Constraint(expr=M.v * ((M.x / M.p) - (M.y / M.p)) == 2)

    M.c_4_ = pyo.Constraint(expr=(M.v * (M.x - M.y)) * (1 / M.p) == 2)

    M.c_5_ = pyo.Constraint(expr=M.v * (M.x - M.y) == 2 * M.p)

    return M
"""


def test_testing1():
    model = models.testing1()

    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing1(data):
    M = pyo.ConcreteModel("testing1")

    M.a = pyo.Var(bounds=(0,1), initialize=0)

    M.b = pyo.Var(bounds=(0,1), initialize=0)

    M.c = pyo.Var(bounds=(0,None))

    M.d = pyo.Var(bounds=(None,0))

    M.e = pyo.Var(initialize=1.0)
    M.e.fix()

    M.q = pyo.Param(mutable=True, initialize=2, within=pyo.Reals)

    M.o = pyo.Objective(expr=(3 * M.a) + M.q)

    M.C_0_ = pyo.Constraint(expr=((3 * M.b) + M.q) - M.a <= 0)

    M.C_1_ = pyo.Constraint(expr=(3 * M.b) + M.b == 0)

    M.C_2_ = pyo.Constraint(expr=((((3 * M.b) * M.a) + M.q) + (M.b * M.b)) + (M.b * M.b) == 0)

    M.C_3_ = pyo.Constraint(expr=((((3 * M.b) * M.b) + M.q) - (M.a * M.b)) - (M.a * M.a) <= 0)

    M.C_4_ = pyo.Constraint(expr=pyo.inequality(-7, ((((3 * M.b) * M.b) + M.q) - (M.a * M.b)) - (M.a * M.a), 7))

    M.C_5_ = pyo.Constraint(expr=M.c + M.d == 0)

    M.C_6_ = pyo.Constraint(expr=M.e + (3 * M.d) == 1)

    M.C_7_ = pyo.Constraint(expr=pyo.inequality(7, ((3 * M.b) + M.q) - M.a, 7))

    return M
"""


def test_testing2():
    model = models.testing2()

    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing2(data):
    M = pyo.ConcreteModel("testing2")

    M.a = pyo.Var(bounds=(0,2), initialize=0)

    M.b = pyo.Var(bounds=(0,1), initialize=1.0)
    M.b.fix()

    M.q = pyo.Param(mutable=True, initialize=2, within=pyo.Reals)

    M.o = pyo.Objective(expr=(((3 * M.a) + M.q) + (((M.a * M.a) * M.a) * ((((-M.a) + M.b) + (3 * M.a)) + (3 * M.b)))) + pyo.sin((-pyo.cos(M.a))))

    return M
"""


# TODO: smk.expression()
def Xtest_testing3():
    model = models.testing3()

    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing3(data):
    M = pyo.ConcreteModel("testing3")

    return M
"""


def test_testing4():
    model = models.testing4()

    assert generate(model=model) == """
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

    M.o = pyo.Objective(expr=(M.a + pyo.cos(M.x)) + pyo.cos(M.y))

    M.c = pyo.Constraint(expr=(M.b + pyo.cos(M.y)) + pyo.cos(M.z) == 1)

    return M
"""


def test_testing5():
    model = models.testing5()

    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing5(data):
    M = pyo.ConcreteModel("testing5")

    M.x = pyo.Var(bounds=(2,2))

    M.o = pyo.Objective(expr=M.x)

    return M
"""


def test_testing6():
    model = models.testing6()

    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing6(data):
    M = pyo.ConcreteModel("testing6")

    M.x = pyo.Var(bounds=(0,1), initialize=0)

    M.p = pyo.Param(mutable=True, initialize=0, within=pyo.Reals)

    M.q = pyo.Param(mutable=True, initialize=2, within=pyo.Reals)

    M.o = pyo.Objective(expr=(((-M.q) * M.x) * M.x) + M.p)

    return M
"""


def test_testing7():
    model = models.testing7()

    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_testing7(data):
    M = pyo.ConcreteModel("testing7")

    M.A = pyo.RangeSet(0, 3)

    M.B = pyo.RangeSet(0, 4)

    M.p = pyo.Param(mutable=True, initialize=0, within=pyo.Reals)

    M.pp = pyo.Param(M.A, mutable=True, initialize=0, within=pyo.Reals)

    M.ppp = pyo.Param(M.A, M.B, mutable=True, initialize=0, within=pyo.Reals)

    M.x = pyo.Var()

    M.xx = pyo.Var(M.A)

    M.xxx = pyo.Var(M.A, M.B)

    M.o = pyo.Objective(expr=M.p * M.x)

    M.c = pyo.Constraint(expr=M.x == 0)

    def cc_(m_,i):
        return m_.pp[i] * m_.xx[i] == 0
    M.cc = pyo.Constraint(M.A, rule=cc_)

    def ccc_(m_,i,j):
        return m_.ppp[i,j] * m_.xxx[i,j] == 0
    M.ccc = pyo.Constraint(M.A, M.B, rule=ccc_)

    return M
"""


def test_simple1():
    model = models.simple1()

    assert generate(model=model) == """
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


def test_hs060():
    model = models.hs060()

    # order = smk.validorder(smk.collect_info(model))
    # assert order == ["N", "x", "o", "c"]

    # print(generate(model=model))
    assert generate(model=model) == """
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


def test_knapsack1():
    model = models.knapsack1(1)

    # order = smk.validorder(smk.collect_info(model))
    # assert order == ["i", "INDEX", "w", "v", "x", "o", "c"]

    # print(generate(model=model))
    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_knapsack1(data):
    M = pyo.ConcreteModel("knapsack1")

    M.INDEX = pyo.RangeSet(0, 9)

    M.w = pyo.Param(M.INDEX, mutable=True, initialize=1.0, within=pyo.Reals)

    M.v = pyo.Param(M.INDEX, mutable=True, initialize=1, within=pyo.Reals)

    M.x = pyo.Var(M.INDEX, bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=sum(M.v[i] * M.x[i] for i in M.INDEX))

    M.c = pyo.Constraint(expr=sum(M.w[i] * M.x[i] for i in M.INDEX) <= 1.0)

    return M
"""


def test_knapsack2():
    model = models.knapsack2(1)

    # order = smk.validorder(smk.collect_info(model))
    # assert order == ["N", "i", "INDEX", "w", "v", "x", "o", "c"]

    # print(generate(model=model))
    assert generate(model=model) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_knapsack2(data):
    M = pyo.ConcreteModel("knapsack2")

    M.N = pyo.Param(mutable=True, initialize=1, within=pyo.Reals)

    M.INDEX = pyo.RangeSet(0, (M.N * 10) - 1)

    M.w = pyo.Param(M.INDEX, mutable=True, initialize=1 / ((M.N * 10) / 10.0), within=pyo.Reals)

    M.v = pyo.Param(M.INDEX, mutable=True, initialize=1, within=pyo.Reals)

    M.x = pyo.Var(M.INDEX, bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=sum(M.v[i] * M.x[i] for i in M.INDEX))

    M.c = pyo.Constraint(expr=sum(M.w[i] * M.x[i] for i in M.INDEX) <= (M.N * 10) / 10.0)

    return M
"""


def test_knapsack3():
    model = models.knapsack3()

    # order = smk.validorder(smk.collect_info(model))
    # assert order == ["N", "i", "INDEX", "w", "v", "x", "o", "c"]

    # print(generate(model=model, data={"N": "int"}))
    assert generate(model=model, data={"N"}) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_knapsack3(data):
    M = pyo.ConcreteModel("knapsack3")

    M.N = pyo.Param(mutable=True, initialize=data["N"], within=pyo.Reals)

    M.INDEX = pyo.RangeSet(0, (M.N * 10) - 1)

    M.w = pyo.Param(M.INDEX, mutable=True, initialize=1 / ((M.N * 10) / 10.0), within=pyo.Reals)

    M.v = pyo.Param(M.INDEX, mutable=True, initialize=1, within=pyo.Reals)

    M.x = pyo.Var(M.INDEX, bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=sum(M.v[i] * M.x[i] for i in M.INDEX))

    M.c = pyo.Constraint(expr=sum(M.w[i] * M.x[i] for i in M.INDEX) <= (M.N * 10) / 10.0)

    return M
"""


def test_knapsack4():
    model = models.knapsack4()

    # print(generate(model=model, data={"N": "int"}))
    assert generate(model=model, data={"ITEMS", "capacity", "value", "weight"}) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_knapsack4(data):
    M = pyo.ConcreteModel("knapsack4")

    M.ITEMS = pyo.Set(initialize=data["ITEMS"])

    M.value = pyo.Param(M.ITEMS, mutable=True, initialize=data["value"], within=pyo.Reals)

    M.weight = pyo.Param(M.ITEMS, mutable=True, initialize=data["weight"], within=pyo.Reals)

    M.capacity = pyo.Param(mutable=True, initialize=data["capacity"], within=pyo.Reals)

    M.x = pyo.Var(M.ITEMS, bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=sum(M.value[i] * M.x[i] for i in M.ITEMS))

    M.c = pyo.Constraint(expr=sum(M.weight[i] * M.x[i] for i in M.ITEMS) <= M.capacity)

    return M
"""


def test_pmedian1():
    model = models.pmedian1()

    # print(generate(model=model, data={"N": "int"}))
    assert generate(model=model, data={"ITEMS", "capacity", "value", "weight"}) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_pmedian1(data):
    M = pyo.ConcreteModel("pmedian1")

    M.N = pyo.RangeSet(0, 9)

    M.M = pyo.RangeSet(0, 9)

    def d_(m_,n,m):
        return 1.0 + (1.0 / ((n + m) + 1))
    M.d = pyo.Param(M.N, M.M, mutable=True, initialize=d_, within=pyo.Reals)

    M.x = pyo.Var(M.N, M.M, bounds=(0.0,1.0), initialize=0.0)

    M.y = pyo.Var(M.N, bounds=(0.0,1.0), initialize=0.0)

    M.o = pyo.Objective(expr=sum(M.d[n,m] * M.x[n,m] for n in M.N for m in M.M))

    def single_x_(m_,m):
        return sum(m_.x[n,m] for n in m_.N) == 1
    M.single_x = pyo.Constraint(M.M, rule=single_x_)

    def bound_y_(m_,n,m):
        return m_.x[n,m] - m_.y[n] <= 0
    M.bound_y = pyo.Constraint(M.N, M.M, rule=bound_y_)

    M.num_facilities = pyo.Constraint(expr=sum(M.y[n] for n in M.N) == 1)

    return M
"""


def test_pmedian2():
    model = models.pmedian2()
    data = {"N": "int"}

    # print(generate(model=model, data=data))
    assert generate(model=model, data=data) == """
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_pmedian2(data):
    M = pyo.ConcreteModel("pmedian2")

    M.N = pyo.RangeSet(0, 9)

    M.M = pyo.RangeSet(0, 9)

    def d_(m_,n,m):
        return 1.0 + (1.0 / ((n + m) + 1))
    M.d = pyo.Param(M.N, M.M, mutable=False, initialize=d_, within=pyo.Reals)

    M.x = pyo.Var(M.N, M.M, bounds=(0.0,1.0), initialize=0.0)

    M.y = pyo.Var(M.N, bounds=(0.0,1.0), initialize=0.0)

    M.o = pyo.Objective(expr=sum(M.d[n,m] * M.x[n,m] for n in M.N for m in M.M))

    def single_x_(m_,m):
        return sum(m_.x[n,m] for n in m_.N) == 1
    M.single_x = pyo.Constraint(M.M, rule=single_x_)

    def bound_y_(m_,n,m):
        return m_.x[n,m] - m_.y[n] <= 0
    M.bound_y = pyo.Constraint(M.N, M.M, rule=bound_y_)

    M.num_facilities = pyo.Constraint(expr=sum(M.y[n] for n in M.N) == 1)

    return M
"""
