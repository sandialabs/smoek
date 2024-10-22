from io import StringIO
import pytest
import smoek as smk
from smoek.core.tests import models
from smoek.pymodel.poek import generate


def test_small1():
    model = models.small1()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 1 -1e+100 1e+100 0
   1:  y 1 -1e+100 1e+100 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( pow(x, 2) )
  Constraints
    0:  pow(y, 2) == 4
"""
    )


def test_small2():
    model = models.small2()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 1 -1e+100 1e+100 0
   1:  y 1 -1e+100 1e+100 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( x )
  Constraints
    0:  pow(y, 2) == 4
"""
    )


def test_small3():
    model = models.small3()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 1 -1e+100 1e+100 0
   1:  y 1 -1e+100 1e+100 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( - ((x)*(y)) )
  Constraints
    0:  pow(y, 2) == 4
"""
    )


def test_small4():
    model = models.small4()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 1 -1e+100 1e+100 0
   1:  y 1 -1e+100 1e+100 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( pow(y, 2) )
  Constraints
    0:  (y)*(x) == 4
"""
    )


def test_small5():
    model = models.small5()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 3
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  v 3 -1 3 0
   1:  x 1 -1 1 0
   2:  y 2 -1 2 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
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
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 4
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  p 2 -1e+100 1e+100 1
   1:  v 3 -1 3 0
   2:  x 1 -1 1 0
   3:  y 2 -1 2 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( x )
  Constraints
    0:  (((1)/(p))*(v))*(x + -1*y) == 2
    1:  ((v)/(p))*(x + -1*y) == 2
    2:  ((v)*(x + -1*y))/(p) == 2
    3:  (v)*((x)/(p) + - ((y)/(p))) == 2
    4:  ((v)*(x + -1*y))*((1)/(p)) == 2
    5:  (v)*(x + -1*y) + -2*p == 0
"""
    )


def test_testing1():
    model = models.testing1()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 5
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  a 0 0 1 0
   1:  b 0 0 1 0
   2:  c nan 0 1e+100 0
   3:  d nan -1e+100 0 0
   4:  e 1 -1e+100 1e+100 1
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  max( 3*a + q )
  Constraints
    0:  3*b + q + -1*a <= 0
    1:  3*b + b == 0
    2:  (3*b)*(a) + q + (b)*(b) + (b)*(b) == 0
    3:  (3*b)*(b) + q + - ((a)*(b)) + - ((a)*(a)) <= 0
    4:  -7 <= (3*b)*(b) + q + - ((a)*(b)) + - ((a)*(a)) <= 7
    5:  c + d == 0
    6:  e + 3*d == 1
    7:  7 <= 3*b + q + -1*a <= 7
"""
    )


def test_testing2():
    model = models.testing2()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  a 0 0 2 0
   1:  b 1 0 1 1
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( 3*a + q + (((a)*(a))*(a))*(-1*a + b + 3*a + 3*b) + sin(- (cos(a))) )
  Constraints
"""
    )


# TODO: smk.expression()
def XXtest_testing3():
    model = models.testing3()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """
"""
    )


def test_testing4():
    model = models.testing4()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 5
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  a 0 0 1 0
   1:  b 0 0 1 0
   2:  x 0 0 1 0
   3:  y 0 0 1 0
   4:  z 0 0 1 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( a + cos(x) + cos(y) )
  Constraints
    0:  b + cos(y) + cos(z) == 1
"""
    )


def test_testing5():
    model = models.testing5()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 1
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x nan 2 2 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( x )
  Constraints
"""
    )


def test_testing6():
    model = models.testing6()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 1
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 0 0 1 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( ((- (q))*(x))*(x) + p )
  Constraints
"""
    )


def test_testing7():
    model = models.testing7()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 25
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x nan -1e+100 1e+100 0
   1:  xx[0] nan -1e+100 1e+100 0
   2:  xx[1] nan -1e+100 1e+100 0
   3:  xx[2] nan -1e+100 1e+100 0
   4:  xx[3] nan -1e+100 1e+100 0
   5:  xxx[0,0] nan -1e+100 1e+100 0
   6:  xxx[0,1] nan -1e+100 1e+100 0
   7:  xxx[0,2] nan -1e+100 1e+100 0
   8:  xxx[0,3] nan -1e+100 1e+100 0
   9:  xxx[0,4] nan -1e+100 1e+100 0
   10:  xxx[1,0] nan -1e+100 1e+100 0
   11:  xxx[1,1] nan -1e+100 1e+100 0
   12:  xxx[1,2] nan -1e+100 1e+100 0
   13:  xxx[1,3] nan -1e+100 1e+100 0
   14:  xxx[1,4] nan -1e+100 1e+100 0
   15:  xxx[2,0] nan -1e+100 1e+100 0
   16:  xxx[2,1] nan -1e+100 1e+100 0
   17:  xxx[2,2] nan -1e+100 1e+100 0
   18:  xxx[2,3] nan -1e+100 1e+100 0
   19:  xxx[2,4] nan -1e+100 1e+100 0
   20:  xxx[3,0] nan -1e+100 1e+100 0
   21:  xxx[3,1] nan -1e+100 1e+100 0
   22:  xxx[3,2] nan -1e+100 1e+100 0
   23:  xxx[3,3] nan -1e+100 1e+100 0
   24:  xxx[3,4] nan -1e+100 1e+100 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( (p)*(x) )
  Constraints
    0:  x == 0
    1:  (pp[0])*(xx[0]) == 0
    2:  (pp[1])*(xx[1]) == 0
    3:  (pp[2])*(xx[2]) == 0
    4:  (pp[3])*(xx[3]) == 0
    5:  (ppp[0,0])*(xxx[0,0]) == 0
    6:  (ppp[0,1])*(xxx[0,1]) == 0
    7:  (ppp[0,2])*(xxx[0,2]) == 0
    8:  (ppp[0,3])*(xxx[0,3]) == 0
    9:  (ppp[0,4])*(xxx[0,4]) == 0
    10:  (ppp[1,0])*(xxx[1,0]) == 0
    11:  (ppp[1,1])*(xxx[1,1]) == 0
    12:  (ppp[1,2])*(xxx[1,2]) == 0
    13:  (ppp[1,3])*(xxx[1,3]) == 0
    14:  (ppp[1,4])*(xxx[1,4]) == 0
    15:  (ppp[2,0])*(xxx[2,0]) == 0
    16:  (ppp[2,1])*(xxx[2,1]) == 0
    17:  (ppp[2,2])*(xxx[2,2]) == 0
    18:  (ppp[2,3])*(xxx[2,3]) == 0
    19:  (ppp[2,4])*(xxx[2,4]) == 0
    20:  (ppp[3,0])*(xxx[3,0]) == 0
    21:  (ppp[3,1])*(xxx[3,1]) == 0
    22:  (ppp[3,2])*(xxx[3,2]) == 0
    23:  (ppp[3,3])*(xxx[3,3]) == 0
    24:  (ppp[3,4])*(xxx[3,4]) == 0
"""
    )


def test_testing8():
    model = models.testing8()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 25
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x 20 -1e+100 1e+100 0
   1:  xx[0] 5 5 5 0
   2:  xx[1] 5 5 5 0
   3:  xx[2] 5 5 5 0
   4:  xx[3] 5 5 5 0
   5:  xxx[0,0] nan -1e+100 1e+100 0
   6:  xxx[0,1] nan -1e+100 1e+100 0
   7:  xxx[0,2] nan -1e+100 1e+100 0
   8:  xxx[0,3] nan -1e+100 1e+100 0
   9:  xxx[0,4] nan -1e+100 1e+100 0
   10:  xxx[1,0] nan -1e+100 1e+100 0
   11:  xxx[1,1] nan -1e+100 1e+100 0
   12:  xxx[1,2] nan -1e+100 1e+100 0
   13:  xxx[1,3] nan -1e+100 1e+100 0
   14:  xxx[1,4] nan -1e+100 1e+100 0
   15:  xxx[2,0] nan -1e+100 1e+100 0
   16:  xxx[2,1] nan -1e+100 1e+100 0
   17:  xxx[2,2] nan -1e+100 1e+100 0
   18:  xxx[2,3] nan -1e+100 1e+100 0
   19:  xxx[2,4] nan -1e+100 1e+100 0
   20:  xxx[3,0] nan -1e+100 1e+100 0
   21:  xxx[3,1] nan -1e+100 1e+100 0
   22:  xxx[3,2] nan -1e+100 1e+100 0
   23:  xxx[3,3] nan -1e+100 1e+100 0
   24:  xxx[3,4] nan -1e+100 1e+100 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( (p)*(x) + xx[0] + xx[1] + xx[2] + xx[3] )
  Constraints
    0:  (pp[0])*(xx[0]) + (pp[1])*(xx[1]) + (pp[2])*(xx[2]) + (pp[3])*(xx[3]) == 0
    1:  (pp[0])*(xx[0]) == 0
    2:  (pp[1])*(xx[1]) == 0
    3:  (pp[2])*(xx[2]) == 0
    4:  (pp[3])*(xx[3]) == 0
    5:  (ppp[0,0])*(xxx[0,0]) + (ppp[1,0])*(xxx[1,0]) + (ppp[2,0])*(xxx[2,0]) + (ppp[3,0])*(xxx[3,0]) == 0
    6:  (ppp[0,1])*(xxx[0,1]) + (ppp[1,1])*(xxx[1,1]) + (ppp[2,1])*(xxx[2,1]) + (ppp[3,1])*(xxx[3,1]) == 0
    7:  (ppp[0,2])*(xxx[0,2]) + (ppp[1,2])*(xxx[1,2]) + (ppp[2,2])*(xxx[2,2]) + (ppp[3,2])*(xxx[3,2]) == 0
    8:  (ppp[0,3])*(xxx[0,3]) + (ppp[1,3])*(xxx[1,3]) + (ppp[2,3])*(xxx[2,3]) + (ppp[3,3])*(xxx[3,3]) == 0
    9:  (ppp[0,4])*(xxx[0,4]) + (ppp[1,4])*(xxx[1,4]) + (ppp[2,4])*(xxx[2,4]) + (ppp[3,4])*(xxx[3,4]) == 0
"""
    )


def test_simple1():
    model = models.simple1()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 2
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x nan 0 1 0
   1:  y nan 0 1 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( x + y )
  Constraints
    0:  x + y == 1
    1:  2*x + y <= 1
    2:  1 <= y + -2*x
"""
    )


def test_hs060():
    model = models.hs060()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 4
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x[1] 2 -10 10 0
   1:  x[2] 2 -10 10 0
   2:  x[3] 2 -10 10 0
   3:  x[4] 2 -10 10 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( pow(x[1] + -1, 2) + pow(x[1] + -1*x[2], 2) + pow(x[2] + -1*x[3], 4) )
  Constraints
    0:  (x[1])*(1 + pow(x[2], 2)) + pow(x[3], 4) == 8.24264
"""
    )


def test_knapsack1():
    model = models.knapsack1()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 10
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x[0] nan 0 1 0
   1:  x[1] nan 0 1 0
   2:  x[2] nan 0 1 0
   3:  x[3] nan 0 1 0
   4:  x[4] nan 0 1 0
   5:  x[5] nan 0 1 0
   6:  x[6] nan 0 1 0
   7:  x[7] nan 0 1 0
   8:  x[8] nan 0 1 0
   9:  x[9] nan 0 1 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  max( (v[0])*(x[0]) + (v[1])*(x[1]) + (v[2])*(x[2]) + (v[3])*(x[3]) + (v[4])*(x[4]) + (v[5])*(x[5]) + (v[6])*(x[6]) + (v[7])*(x[7]) + (v[8])*(x[8]) + (v[9])*(x[9]) )
  Constraints
    0:  (w[0])*(x[0]) + (w[1])*(x[1]) + (w[2])*(x[2]) + (w[3])*(x[3]) + (w[4])*(x[4]) + (w[5])*(x[5]) + (w[6])*(x[6]) + (w[7])*(x[7]) + (w[8])*(x[8]) + (w[9])*(x[9]) <= 1
"""
    )


def test_knapsack2():
    model = models.knapsack2()
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 10
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x[0] nan 0 1 0
   1:  x[1] nan 0 1 0
   2:  x[2] nan 0 1 0
   3:  x[3] nan 0 1 0
   4:  x[4] nan 0 1 0
   5:  x[5] nan 0 1 0
   6:  x[6] nan 0 1 0
   7:  x[7] nan 0 1 0
   8:  x[8] nan 0 1 0
   9:  x[9] nan 0 1 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  max( (v[0])*(x[0]) + (v[1])*(x[1]) + (v[2])*(x[2]) + (v[3])*(x[3]) + (v[4])*(x[4]) + (v[5])*(x[5]) + (v[6])*(x[6]) + (v[7])*(x[7]) + (v[8])*(x[8]) + (v[9])*(x[9]) )
  Constraints
    0:  (w[0])*(x[0]) + (w[1])*(x[1]) + (w[2])*(x[2]) + (w[3])*(x[3]) + (w[4])*(x[4]) + (w[5])*(x[5]) + (w[6])*(x[6]) + (w[7])*(x[7]) + (w[8])*(x[8]) + (w[9])*(x[9]) <= ((N)*(10))/(10)
"""
    )


def test_knapsack3():
    model = models.knapsack3()
    data = {"N": 1}
    m = generate(model=model, data=data)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 10
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x[0] nan 0 1 0
   1:  x[1] nan 0 1 0
   2:  x[2] nan 0 1 0
   3:  x[3] nan 0 1 0
   4:  x[4] nan 0 1 0
   5:  x[5] nan 0 1 0
   6:  x[6] nan 0 1 0
   7:  x[7] nan 0 1 0
   8:  x[8] nan 0 1 0
   9:  x[9] nan 0 1 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  max( (v[0])*(x[0]) + (v[1])*(x[1]) + (v[2])*(x[2]) + (v[3])*(x[3]) + (v[4])*(x[4]) + (v[5])*(x[5]) + (v[6])*(x[6]) + (v[7])*(x[7]) + (v[8])*(x[8]) + (v[9])*(x[9]) )
  Constraints
    0:  (w[0])*(x[0]) + (w[1])*(x[1]) + (w[2])*(x[2]) + (w[3])*(x[3]) + (w[4])*(x[4]) + (w[5])*(x[5]) + (w[6])*(x[6]) + (w[7])*(x[7]) + (w[8])*(x[8]) + (w[9])*(x[9]) <= ((N)*(10))/(10)
"""
    )


def test_knapsack4():
    model = models.knapsack4()
    data = {
        "ITEMS": [1, 2, 3, 4],
        "capacity": 14,
        "value": {1: 8, 2: 3, 3: 6, 4: 11},
        "weight": {1: 5, 2: 7, 3: 4, 4: 3},
    }
    m = generate(model=model, data=data)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 4
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x[1] nan 0 1 0
   1:  x[2] nan 0 1 0
   2:  x[3] nan 0 1 0
   3:  x[4] nan 0 1 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  max( (value[1])*(x[1]) + (value[2])*(x[2]) + (value[3])*(x[3]) + (value[4])*(x[4]) )
  Constraints
    0:  (weight[1])*(x[1]) + (weight[2])*(x[2]) + (weight[3])*(x[3]) + (weight[4])*(x[4]) <= capacity
"""
    )


def test_pmedian1():
    model = models.pmedian1(5)
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 30
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x[0,0] 0 0 1 0
   1:  x[0,1] 0 0 1 0
   2:  x[0,2] 0 0 1 0
   3:  x[0,3] 0 0 1 0
   4:  x[0,4] 0 0 1 0
   5:  x[1,0] 0 0 1 0
   6:  x[1,1] 0 0 1 0
   7:  x[1,2] 0 0 1 0
   8:  x[1,3] 0 0 1 0
   9:  x[1,4] 0 0 1 0
   10:  x[2,0] 0 0 1 0
   11:  x[2,1] 0 0 1 0
   12:  x[2,2] 0 0 1 0
   13:  x[2,3] 0 0 1 0
   14:  x[2,4] 0 0 1 0
   15:  x[3,0] 0 0 1 0
   16:  x[3,1] 0 0 1 0
   17:  x[3,2] 0 0 1 0
   18:  x[3,3] 0 0 1 0
   19:  x[3,4] 0 0 1 0
   20:  x[4,0] 0 0 1 0
   21:  x[4,1] 0 0 1 0
   22:  x[4,2] 0 0 1 0
   23:  x[4,3] 0 0 1 0
   24:  x[4,4] 0 0 1 0
   25:  y[0] 0 0 1 0
   26:  y[1] 0 0 1 0
   27:  y[2] 0 0 1 0
   28:  y[3] 0 0 1 0
   29:  y[4] 0 0 1 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( (d[0,0])*(x[0,0]) + (d[0,1])*(x[0,1]) + (d[0,2])*(x[0,2]) + (d[0,3])*(x[0,3]) + (d[0,4])*(x[0,4]) + (d[1,0])*(x[1,0]) + (d[1,1])*(x[1,1]) + (d[1,2])*(x[1,2]) + (d[1,3])*(x[1,3]) + (d[1,4])*(x[1,4]) + (d[2,0])*(x[2,0]) + (d[2,1])*(x[2,1]) + (d[2,2])*(x[2,2]) + (d[2,3])*(x[2,3]) + (d[2,4])*(x[2,4]) + (d[3,0])*(x[3,0]) + (d[3,1])*(x[3,1]) + (d[3,2])*(x[3,2]) + (d[3,3])*(x[3,3]) + (d[3,4])*(x[3,4]) + (d[4,0])*(x[4,0]) + (d[4,1])*(x[4,1]) + (d[4,2])*(x[4,2]) + (d[4,3])*(x[4,3]) + (d[4,4])*(x[4,4]) )
  Constraints
    0:  x[0,0] + x[1,0] + x[2,0] + x[3,0] + x[4,0] == 1
    1:  x[0,1] + x[1,1] + x[2,1] + x[3,1] + x[4,1] == 1
    2:  x[0,2] + x[1,2] + x[2,2] + x[3,2] + x[4,2] == 1
    3:  x[0,3] + x[1,3] + x[2,3] + x[3,3] + x[4,3] == 1
    4:  x[0,4] + x[1,4] + x[2,4] + x[3,4] + x[4,4] == 1
    5:  x[0,0] + - (y[0]) <= 0
    6:  x[0,1] + - (y[0]) <= 0
    7:  x[0,2] + - (y[0]) <= 0
    8:  x[0,3] + - (y[0]) <= 0
    9:  x[0,4] + - (y[0]) <= 0
    10:  x[1,0] + - (y[1]) <= 0
    11:  x[1,1] + - (y[1]) <= 0
    12:  x[1,2] + - (y[1]) <= 0
    13:  x[1,3] + - (y[1]) <= 0
    14:  x[1,4] + - (y[1]) <= 0
    15:  x[2,0] + - (y[2]) <= 0
    16:  x[2,1] + - (y[2]) <= 0
    17:  x[2,2] + - (y[2]) <= 0
    18:  x[2,3] + - (y[2]) <= 0
    19:  x[2,4] + - (y[2]) <= 0
    20:  x[3,0] + - (y[3]) <= 0
    21:  x[3,1] + - (y[3]) <= 0
    22:  x[3,2] + - (y[3]) <= 0
    23:  x[3,3] + - (y[3]) <= 0
    24:  x[3,4] + - (y[3]) <= 0
    25:  x[4,0] + - (y[4]) <= 0
    26:  x[4,1] + - (y[4]) <= 0
    27:  x[4,2] + - (y[4]) <= 0
    28:  x[4,3] + - (y[4]) <= 0
    29:  x[4,4] + - (y[4]) <= 0
    30:  y[0] + y[1] + y[2] + y[3] + y[4] == 1
"""
    )


def test_pmedian2():
    model = models.pmedian2(5)
    m = generate(model=model)
    M = m.expand()
    M.generate_names()

    # M.print_values()
    out = StringIO()
    M.print_values(ostream=out)
    assert (
        out.getvalue()
        == """Model Variables: 30
   (<Index>: <Name> <Value> <LB> <UB> <Fixed>)
   0:  x[0,0] 0 0 1 0
   1:  x[0,1] 0 0 1 0
   2:  x[0,2] 0 0 1 0
   3:  x[0,3] 0 0 1 0
   4:  x[0,4] 0 0 1 0
   5:  x[1,0] 0 0 1 0
   6:  x[1,1] 0 0 1 0
   7:  x[1,2] 0 0 1 0
   8:  x[1,3] 0 0 1 0
   9:  x[1,4] 0 0 1 0
   10:  x[2,0] 0 0 1 0
   11:  x[2,1] 0 0 1 0
   12:  x[2,2] 0 0 1 0
   13:  x[2,3] 0 0 1 0
   14:  x[2,4] 0 0 1 0
   15:  x[3,0] 0 0 1 0
   16:  x[3,1] 0 0 1 0
   17:  x[3,2] 0 0 1 0
   18:  x[3,3] 0 0 1 0
   19:  x[3,4] 0 0 1 0
   20:  x[4,0] 0 0 1 0
   21:  x[4,1] 0 0 1 0
   22:  x[4,2] 0 0 1 0
   23:  x[4,3] 0 0 1 0
   24:  x[4,4] 0 0 1 0
   25:  y[0] 0 0 1 0
   26:  y[1] 0 0 1 0
   27:  y[2] 0 0 1 0
   28:  y[3] 0 0 1 0
   29:  y[4] 0 0 1 0
"""
    )

    # M.print_equations()
    out = StringIO()
    M.print_equations(ostream=out)
    assert (
        out.getvalue()
        == """MODEL
  Objectives
    0:  min( (2)*(x[0,0]) + (1.5)*(x[0,1]) + (1.33333)*(x[0,2]) + (1.25)*(x[0,3]) + (1.2)*(x[0,4]) + (1.5)*(x[1,0]) + (1.33333)*(x[1,1]) + (1.25)*(x[1,2]) + (1.2)*(x[1,3]) + (1.16667)*(x[1,4]) + (1.33333)*(x[2,0]) + (1.25)*(x[2,1]) + (1.2)*(x[2,2]) + (1.16667)*(x[2,3]) + (1.14286)*(x[2,4]) + (1.25)*(x[3,0]) + (1.2)*(x[3,1]) + (1.16667)*(x[3,2]) + (1.14286)*(x[3,3]) + (1.125)*(x[3,4]) + (1.2)*(x[4,0]) + (1.16667)*(x[4,1]) + (1.14286)*(x[4,2]) + (1.125)*(x[4,3]) + (1.11111)*(x[4,4]) )
  Constraints
    0:  x[0,0] + x[1,0] + x[2,0] + x[3,0] + x[4,0] == 1
    1:  x[0,1] + x[1,1] + x[2,1] + x[3,1] + x[4,1] == 1
    2:  x[0,2] + x[1,2] + x[2,2] + x[3,2] + x[4,2] == 1
    3:  x[0,3] + x[1,3] + x[2,3] + x[3,3] + x[4,3] == 1
    4:  x[0,4] + x[1,4] + x[2,4] + x[3,4] + x[4,4] == 1
    5:  x[0,0] + - (y[0]) <= 0
    6:  x[0,1] + - (y[0]) <= 0
    7:  x[0,2] + - (y[0]) <= 0
    8:  x[0,3] + - (y[0]) <= 0
    9:  x[0,4] + - (y[0]) <= 0
    10:  x[1,0] + - (y[1]) <= 0
    11:  x[1,1] + - (y[1]) <= 0
    12:  x[1,2] + - (y[1]) <= 0
    13:  x[1,3] + - (y[1]) <= 0
    14:  x[1,4] + - (y[1]) <= 0
    15:  x[2,0] + - (y[2]) <= 0
    16:  x[2,1] + - (y[2]) <= 0
    17:  x[2,2] + - (y[2]) <= 0
    18:  x[2,3] + - (y[2]) <= 0
    19:  x[2,4] + - (y[2]) <= 0
    20:  x[3,0] + - (y[3]) <= 0
    21:  x[3,1] + - (y[3]) <= 0
    22:  x[3,2] + - (y[3]) <= 0
    23:  x[3,3] + - (y[3]) <= 0
    24:  x[3,4] + - (y[3]) <= 0
    25:  x[4,0] + - (y[4]) <= 0
    26:  x[4,1] + - (y[4]) <= 0
    27:  x[4,2] + - (y[4]) <= 0
    28:  x[4,3] + - (y[4]) <= 0
    29:  x[4,4] + - (y[4]) <= 0
    30:  y[0] + y[1] + y[2] + y[3] + y[4] == 1
"""
    )
