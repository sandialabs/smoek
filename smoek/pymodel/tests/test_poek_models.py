from io import StringIO
import pytest
import smoek as smk
from smoek.core.tests import models
from smoek.pymodel.poek import generate


def test_small1():
    model = models.small1()
    M = generate(model=model)

    #M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 1 -1e+100 1e+100 0
   1:  y 1 -1e+100 1e+100 0
"""
    )

    #M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert(
        out.getvalue() == """MODEL
  Objectives
    0:  min( pow(x, 2) )
  Constraints
    0:  pow(y, 2) == 4
""")


def test_small2():
    model = models.small2()
    M = generate(model=model)

    #M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 1 -1e+100 1e+100 0
   1:  y 1 -1e+100 1e+100 0
"""
    )

    #M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """MODEL
  Objectives
    0:  min( x )
  Constraints
    0:  pow(y, 2) == 4
"""
    )


def test_small3():
    model = models.small3()
    M = generate(model=model)

    #M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 1 -1e+100 1e+100 0
   1:  y 1 -1e+100 1e+100 0
"""
    )

    #M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """MODEL
  Objectives
    0:  min( - ((x)*(y)) )
  Constraints
    0:  pow(y, 2) == 4
"""
    )


def test_small4():
    model = models.small4()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 1 -1e+100 1e+100 0
   1:  y 1 -1e+100 1e+100 0
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """MODEL
  Objectives
    0:  min( pow(y, 2) )
  Constraints
    0:  (y)*(x) == 4
"""
    )


def test_small5():
    model = models.small5()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """Model Variables: 3
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  v 3 -1 3 0
   1:  x 1 -1 1 0
   2:  y 2 -1 2 0
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """MODEL
  Objectives
    0:  min( (pow(x, 2))/(2) + (pow(x, 2))/(q) )
  Constraints
    0:  (0.5*v)*(x + -1*y) == 2
    1:  (0.5*v)*(x + -1*y) == 2
    2:  ((v)*(x + -1*y))/(2) == 2
    3:  (v)*(0.5*x + -0.5*y) == 2
    4:  ((v)*(x + -1*y))*(0.5) == 2
    5:  (v)*(x + -1*y) == 4
    6:  (((1)/(q))*(v))*(x + -1*y) == 2
    7:  ((v)/(q))*(x + -1*y) == 2
    8:  ((v)*(x + -1*y))/(q) == 2
    9:  (v)*(0.5*x + - ((y)/(q))) == 2
    10:  ((v)*(x + -1*y))*((1)/(q)) == 2
    11:  (v)*(x + -1*y) == (2)*(q)
"""
    )


def test_small6():
    model = models.small6()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """Model Variables: 4
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  _v0 1 -1 1 0
   1:  _v1 2 -1 2 0
   2:  _v2 3 -1 3 0
   3:  _v3 2 -1e+100 1e+100 1
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """MODEL
  Objectives
    0:  min( _v0 )
  Constraints
    0:  (((1)/(_v3))*(_v2))*(_v0 + -1*_v1) == 2
    1:  ((_v2)/(_v3))*(_v0 + -1*_v1) == 2
    2:  ((_v2)*(_v0 + -1*_v1))/(_v3) == 2
    3:  (_v2)*((_v0)/(_v3) + - ((_v1)/(_v3))) == 2
    4:  ((_v2)*(_v0 + -1*_v1))*((1)/(_v3)) == 2
    5:  (_v2)*(_v0 + -1*_v1) + -2*_v3 == 0
"""
    )


def test_testing1():
    model = models.testing1()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_testing2():
    model = models.testing2()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


# TODO: smk.expression()
def XXtest_testing3():
    model = models.testing3()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_testing4():
    model = models.testing4()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_testing5():
    model = models.testing5()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_testing6():
    model = models.testing6()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_testing7():
    model = models.testing7()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_testing8():
    model = models.testing8()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )

def test_simple1():
    model = models.simple1()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_hs060():
    model = models.hs060()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_knapsack1():
    model = models.knapsack1()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_knapsack2():
    model = models.knapsack2()
    M = generate(model=model)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_knapsack3():
    model = models.knapsack3()
    data = {"N": 1}
    M = generate(model=model,data=data)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )


def test_knapsack4():
    model = models.knapsack4()
    data = {"ITEMS":[1,2,3,4], "capacity":14, "value":{1:8, 2:3, 3:6, 4:11}, "weight":{1:5, 2:7, 3:4, 4:3}}
    M = generate(model=model, data=data)

    M.print_values()
    out = StringIO()
    M.print_values(ostream=out) 
    assert(
        out.getvalue() == """
"""
    )

    M.print_equations() 
    out = StringIO()
    M.print_equations(ostream=out) 
    assert (
        out.getvalue() == """
"""
    )
