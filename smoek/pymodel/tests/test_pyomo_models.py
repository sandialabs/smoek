from io import StringIO
import pytest
import smoek as smk
from smoek.core.tests import models
from smoek.pymodel.pyomo import generate


def test_small1():
    model = models.small1()
    M = generate(model=model)
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 Var Declarations
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :   1.0 :  None : False : False :  Reals
    y : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :   1.0 :  None : False : False :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize :       x**2

1 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body : Upper : Active
        None :   4.0 : y**2 :   4.0 :   True

4 Declarations: x y o c
"""
    )


def test_small2():
    model = models.small2()
    M = generate(model=model)
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 Var Declarations
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :   1.0 :  None : False : False :  Reals
    y : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :   1.0 :  None : False : False :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize :          x

1 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body : Upper : Active
        None :   4.0 : y**2 :   4.0 :   True

4 Declarations: x y o c
"""
    )


def test_small3():
    model = models.small3()
    M = generate(model=model)
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 Var Declarations
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :   1.0 :  None : False : False :  Reals
    y : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :   1.0 :  None : False : False :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : - x*y

1 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body : Upper : Active
        None :   4.0 : y**2 :   4.0 :   True

4 Declarations: x y o c
"""
    )


def test_small4():
    model = models.small4()
    M = generate(model=model)
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 Var Declarations
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :   1.0 :  None : False : False :  Reals
    y : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :   1.0 :  None : False : False :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize :       y**2

1 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body : Upper : Active
        None :   4.0 :  y*x :   4.0 :   True

4 Declarations: x y o c
"""
    )


def test_small5():
    model = models.small5()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """1 Param Declarations
    q : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :     2

3 Var Declarations
    v : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :    -1 :   3.0 :     3 : False : False :  Reals
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :    -1 :   1.0 :     1 : False : False :  Reals
    y : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :    -1 :   2.0 :     2 : False : False :  Reals

1 Objective Declarations
    _o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : x**2/2.0 + x**2/q

12 Constraint Declarations
    _c0 : Size=1, Index=None, Active=True
        Key  : Lower : Body          : Upper : Active
        None :   2.0 : 0.5*v*(x - y) :   2.0 :   True
    _c1 : Size=1, Index=None, Active=True
        Key  : Lower : Body          : Upper : Active
        None :   2.0 : 0.5*v*(x - y) :   2.0 :   True
    _c10 : Size=1, Index=None, Active=True
        Key  : Lower : Body            : Upper : Active
        None :   2.0 : v*(x - y)*(1/q) :   2.0 :   True
    _c11 : Size=1, Index=None, Active=True
        Key  : Lower : Body      : Upper : Active
        None :   2*q : v*(x - y) :   2*q :   True
    _c2 : Size=1, Index=None, Active=True
        Key  : Lower : Body          : Upper : Active
        None :   2.0 : v*(x - y)/2.0 :   2.0 :   True
    _c3 : Size=1, Index=None, Active=True
        Key  : Lower : Body              : Upper : Active
        None :   2.0 : v*(0.5*x - 0.5*y) :   2.0 :   True
    _c4 : Size=1, Index=None, Active=True
        Key  : Lower : Body          : Upper : Active
        None :   2.0 : v*(x - y)*0.5 :   2.0 :   True
    _c5 : Size=1, Index=None, Active=True
        Key  : Lower : Body      : Upper : Active
        None :   4.0 : v*(x - y) :   4.0 :   True
    _c6 : Size=1, Index=None, Active=True
        Key  : Lower : Body          : Upper : Active
        None :   2.0 : 1/q*v*(x - y) :   2.0 :   True
    _c7 : Size=1, Index=None, Active=True
        Key  : Lower : Body          : Upper : Active
        None :   2.0 : 1/q*v*(x - y) :   2.0 :   True
    _c8 : Size=1, Index=None, Active=True
        Key  : Lower : Body        : Upper : Active
        None :   2.0 : v*(x - y)/q :   2.0 :   True
    _c9 : Size=1, Index=None, Active=True
        Key  : Lower : Body              : Upper : Active
        None :   2.0 : v*(0.5*x - 1/q*y) :   2.0 :   True

17 Declarations: x y v q _o _c0 _c1 _c2 _c3 _c4 _c5 _c6 _c7 _c8 _c9 _c10 _c11
"""
    )


def test_small6():
    model = models.small6()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """4 Var Declarations
    _v0 : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :    -1 :     1 :     1 : False : False :  Reals
    _v1 : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :    -1 :     2 :     2 : False : False :  Reals
    _v2 : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :    -1 :     3 :     3 : False : False :  Reals
    _v3 : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :     2 :  None :  True : False :  Reals

1 Objective Declarations
    _o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize :        _v0

6 Constraint Declarations
    _c0 : Size=1, Index=None, Active=True
        Key  : Lower : Body                  : Upper : Active
        None :   2.0 : 1/_v3*_v2*(_v0 - _v1) :   2.0 :   True
    _c1 : Size=1, Index=None, Active=True
        Key  : Lower : Body                : Upper : Active
        None :   2.0 : _v2/_v3*(_v0 - _v1) :   2.0 :   True
    _c2 : Size=1, Index=None, Active=True
        Key  : Lower : Body                : Upper : Active
        None :   2.0 : _v2*(_v0 - _v1)/_v3 :   2.0 :   True
    _c3 : Size=1, Index=None, Active=True
        Key  : Lower : Body                    : Upper : Active
        None :   2.0 : _v2*(_v0/_v3 - _v1/_v3) :   2.0 :   True
    _c4 : Size=1, Index=None, Active=True
        Key  : Lower : Body                    : Upper : Active
        None :   2.0 : _v2*(_v0 - _v1)*(1/_v3) :   2.0 :   True
    _c5 : Size=1, Index=None, Active=True
        Key  : Lower : Body                    : Upper : Active
        None :   0.0 : 2*_v3 - _v2*(_v0 - _v1) :   0.0 :   True

11 Declarations: _v0 _v1 _v2 _v3 _o _c0 _c1 _c2 _c3 _c4 _c5
"""
    )


def test_testing1():
    model = models.testing1()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """1 Param Declarations
    q : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :     2

5 Var Declarations
    _v2 : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :  None :  None : False :  True :  Reals
    _v3 : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :  None :     0 : False :  True :  Reals
    a : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :     0 :     1 : False : False : Integers
    b : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :     0 :     1 : False : False : Binary
    e : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :   1.0 :  None :  True : False :  Reals

1 Objective Declarations
    _o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : 3*a + q

8 Constraint Declarations
    _c0 : Size=1, Index=None, Active=True
        Key  : Lower : Body        : Upper : Active
        None :  -Inf : 3*b + q - a :   0.0 :   True
    _c1 : Size=1, Index=None, Active=True
        Key  : Lower : Body    : Upper : Active
        None :   0.0 : 3*b + b :   0.0 :   True
    _c2 : Size=1, Index=None, Active=True
        Key  : Lower : Body                  : Upper : Active
        None :   0.0 : 3*b*a + q + b*b + b*b :   0.0 :   True
    _c3 : Size=1, Index=None, Active=True
        Key  : Lower : Body                  : Upper : Active
        None :  -Inf : 3*b*b + q - a*b - a*a :   0.0 :   True
    _c4 : Size=1, Index=None, Active=True
        Key  : Lower : Body                  : Upper : Active
        None :  -7.0 : 3*b*b + q - a*b - a*a :   7.0 :   True
    _c5 : Size=1, Index=None, Active=True
        Key  : Lower : Body      : Upper : Active
        None :   0.0 : _v2 + _v3 :   0.0 :   True
    _c6 : Size=1, Index=None, Active=True
        Key  : Lower : Body      : Upper : Active
        None :   1.0 : e + 3*_v3 :   1.0 :   True
    _c7 : Size=1, Index=None, Active=True
        Key  : Lower : Body        : Upper : Active
        None :   7.0 : 3*b + q - a :   7.0 :   True

15 Declarations: a b _v2 _v3 e q _o _c0 _c1 _c2 _c3 _c4 _c5 _c6 _c7
"""
    )


def test_testing2():
    model = models.testing2()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """1 Param Declarations
    q : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :     2

2 Var Declarations
    a : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :     0 :     2 : False : False : Integers
    b : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :   1.0 :     1 :  True : False : Binary

1 Objective Declarations
    _o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : 3*a + q + a*a*a*(- a + b + 3*a + 3*b) + sin(- cos(a))

4 Declarations: a b q _o
"""
    )


# TODO: smk.expression()
def XXtest_testing3():
    model = models.testing3()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """
"""
    )


def test_testing4():
    model = models.testing4()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """5 Var Declarations
    a : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :     0 :     1 : False : False : Integers
    b : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :     0 :     1 : False : False : Binary
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :     0 :     1 : False : False : Binary
    y : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :     0 :     1 : False : False : Binary
    z : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :     0 :     1 : False : False : Binary

1 Objective Declarations
    _o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : a + cos(x) + cos(y)

1 Constraint Declarations
    _c0 : Size=1, Index=None, Active=True
        Key  : Lower : Body                : Upper : Active
        None :   1.0 : b + cos(y) + cos(z) :   1.0 :   True

7 Declarations: x y z a b _o _c0
"""
    )


def test_testing5():
    model = models.testing5()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """1 Var Declarations
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     2 :  None :     2 : False :  True :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize :          x

2 Declarations: x o
"""
    )


def test_testing6():
    model = models.testing6()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 Param Declarations
    p : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :     0
    q : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :     2

1 Var Declarations
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     0 :     0 :     1 : False : False :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : - q*x*x + p

4 Declarations: x p q o
"""
    )


def test_testing7():
    model = models.testing7()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 RangeSet Declarations
    A : Dimen=1, Size=4, Bounds=(0, 3)
        Key  : Finite : Members
        None :   True :   [0:3]
    B : Dimen=1, Size=5, Bounds=(0, 4)
        Key  : Finite : Members
        None :   True :   [0:4]

3 Param Declarations
    p : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :     0
    pp : Size=4, Index=A, Domain=Reals, Default=None, Mutable=True
        Key : Value
          0 :     0
          1 :     0
          2 :     0
          3 :     0
    ppp : Size=20, Index=A*B, Domain=Reals, Default=None, Mutable=True
        Key    : Value
        (0, 0) :     0
        (0, 1) :     0
        (0, 2) :     0
        (0, 3) :     0
        (0, 4) :     0
        (1, 0) :     0
        (1, 1) :     0
        (1, 2) :     0
        (1, 3) :     0
        (1, 4) :     0
        (2, 0) :     0
        (2, 1) :     0
        (2, 2) :     0
        (2, 3) :     0
        (2, 4) :     0
        (3, 0) :     0
        (3, 1) :     0
        (3, 2) :     0
        (3, 3) :     0
        (3, 4) :     0

3 Var Declarations
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :  None :  None : False :  True :  Reals
    xx : Size=4, Index=A
        Key : Lower : Value : Upper : Fixed : Stale : Domain
          0 :  None :  None :  None : False :  True :  Reals
          1 :  None :  None :  None : False :  True :  Reals
          2 :  None :  None :  None : False :  True :  Reals
          3 :  None :  None :  None : False :  True :  Reals
    xxx : Size=20, Index=A*B
        Key    : Lower : Value : Upper : Fixed : Stale : Domain
        (0, 0) :  None :  None :  None : False :  True :  Reals
        (0, 1) :  None :  None :  None : False :  True :  Reals
        (0, 2) :  None :  None :  None : False :  True :  Reals
        (0, 3) :  None :  None :  None : False :  True :  Reals
        (0, 4) :  None :  None :  None : False :  True :  Reals
        (1, 0) :  None :  None :  None : False :  True :  Reals
        (1, 1) :  None :  None :  None : False :  True :  Reals
        (1, 2) :  None :  None :  None : False :  True :  Reals
        (1, 3) :  None :  None :  None : False :  True :  Reals
        (1, 4) :  None :  None :  None : False :  True :  Reals
        (2, 0) :  None :  None :  None : False :  True :  Reals
        (2, 1) :  None :  None :  None : False :  True :  Reals
        (2, 2) :  None :  None :  None : False :  True :  Reals
        (2, 3) :  None :  None :  None : False :  True :  Reals
        (2, 4) :  None :  None :  None : False :  True :  Reals
        (3, 0) :  None :  None :  None : False :  True :  Reals
        (3, 1) :  None :  None :  None : False :  True :  Reals
        (3, 2) :  None :  None :  None : False :  True :  Reals
        (3, 3) :  None :  None :  None : False :  True :  Reals
        (3, 4) :  None :  None :  None : False :  True :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize :        p*x

3 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body : Upper : Active
        None :   0.0 :    x :   0.0 :   True
    cc : Size=4, Index=A, Active=True
        Key : Lower : Body        : Upper : Active
          0 :   0.0 : pp[0]*xx[0] :   0.0 :   True
          1 :   0.0 : pp[1]*xx[1] :   0.0 :   True
          2 :   0.0 : pp[2]*xx[2] :   0.0 :   True
          3 :   0.0 : pp[3]*xx[3] :   0.0 :   True
    ccc : Size=20, Index=A*B, Active=True
        Key    : Lower : Body              : Upper : Active
        (0, 0) :   0.0 : ppp[0,0]*xxx[0,0] :   0.0 :   True
        (0, 1) :   0.0 : ppp[0,1]*xxx[0,1] :   0.0 :   True
        (0, 2) :   0.0 : ppp[0,2]*xxx[0,2] :   0.0 :   True
        (0, 3) :   0.0 : ppp[0,3]*xxx[0,3] :   0.0 :   True
        (0, 4) :   0.0 : ppp[0,4]*xxx[0,4] :   0.0 :   True
        (1, 0) :   0.0 : ppp[1,0]*xxx[1,0] :   0.0 :   True
        (1, 1) :   0.0 : ppp[1,1]*xxx[1,1] :   0.0 :   True
        (1, 2) :   0.0 : ppp[1,2]*xxx[1,2] :   0.0 :   True
        (1, 3) :   0.0 : ppp[1,3]*xxx[1,3] :   0.0 :   True
        (1, 4) :   0.0 : ppp[1,4]*xxx[1,4] :   0.0 :   True
        (2, 0) :   0.0 : ppp[2,0]*xxx[2,0] :   0.0 :   True
        (2, 1) :   0.0 : ppp[2,1]*xxx[2,1] :   0.0 :   True
        (2, 2) :   0.0 : ppp[2,2]*xxx[2,2] :   0.0 :   True
        (2, 3) :   0.0 : ppp[2,3]*xxx[2,3] :   0.0 :   True
        (2, 4) :   0.0 : ppp[2,4]*xxx[2,4] :   0.0 :   True
        (3, 0) :   0.0 : ppp[3,0]*xxx[3,0] :   0.0 :   True
        (3, 1) :   0.0 : ppp[3,1]*xxx[3,1] :   0.0 :   True
        (3, 2) :   0.0 : ppp[3,2]*xxx[3,2] :   0.0 :   True
        (3, 3) :   0.0 : ppp[3,3]*xxx[3,3] :   0.0 :   True
        (3, 4) :   0.0 : ppp[3,4]*xxx[3,4] :   0.0 :   True

12 Declarations: A B p pp ppp x xx xxx o c cc ccc
"""
    )


def test_testing8():
    model = models.testing8()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 RangeSet Declarations
    A : Dimen=1, Size=4, Bounds=(0, 3)
        Key  : Finite : Members
        None :   True :   [0:3]
    B : Dimen=1, Size=5, Bounds=(0, 4)
        Key  : Finite : Members
        None :   True :   [0:4]

3 Param Declarations
    p : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :    20
    pp : Size=4, Index=A, Domain=Reals, Default=None, Mutable=True
        Key : Value
          0 :     5
          1 :     5
          2 :     5
          3 :     5
    ppp : Size=20, Index=A*B, Domain=Reals, Default=None, Mutable=True
        Key    : Value
        (0, 0) :     1
        (0, 1) :     1
        (0, 2) :     1
        (0, 3) :     1
        (0, 4) :     1
        (1, 0) :     1
        (1, 1) :     1
        (1, 2) :     1
        (1, 3) :     1
        (1, 4) :     1
        (2, 0) :     1
        (2, 1) :     1
        (2, 2) :     1
        (2, 3) :     1
        (2, 4) :     1
        (3, 0) :     1
        (3, 1) :     1
        (3, 2) :     1
        (3, 3) :     1
        (3, 4) :     1

3 Var Declarations
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :  None :    20 :  None : False : False :  Reals
    xx : Size=4, Index=A
        Key : Lower : Value : Upper : Fixed : Stale : Domain
          0 :   5.0 :     5 :   5.0 : False : False :  Reals
          1 :   5.0 :     5 :   5.0 : False : False :  Reals
          2 :   5.0 :     5 :   5.0 : False : False :  Reals
          3 :   5.0 :     5 :   5.0 : False : False :  Reals
    xxx : Size=20, Index=A*B
        Key    : Lower : Value : Upper : Fixed : Stale : Domain
        (0, 0) :  None :  None :  None : False :  True :  Reals
        (0, 1) :  None :  None :  None : False :  True :  Reals
        (0, 2) :  None :  None :  None : False :  True :  Reals
        (0, 3) :  None :  None :  None : False :  True :  Reals
        (0, 4) :  None :  None :  None : False :  True :  Reals
        (1, 0) :  None :  None :  None : False :  True :  Reals
        (1, 1) :  None :  None :  None : False :  True :  Reals
        (1, 2) :  None :  None :  None : False :  True :  Reals
        (1, 3) :  None :  None :  None : False :  True :  Reals
        (1, 4) :  None :  None :  None : False :  True :  Reals
        (2, 0) :  None :  None :  None : False :  True :  Reals
        (2, 1) :  None :  None :  None : False :  True :  Reals
        (2, 2) :  None :  None :  None : False :  True :  Reals
        (2, 3) :  None :  None :  None : False :  True :  Reals
        (2, 4) :  None :  None :  None : False :  True :  Reals
        (3, 0) :  None :  None :  None : False :  True :  Reals
        (3, 1) :  None :  None :  None : False :  True :  Reals
        (3, 2) :  None :  None :  None : False :  True :  Reals
        (3, 3) :  None :  None :  None : False :  True :  Reals
        (3, 4) :  None :  None :  None : False :  True :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : xx[0] + xx[1] + xx[2] + xx[3] + p*x

3 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body                                                  : Upper : Active
        None :   0.0 : pp[0]*xx[0] + pp[1]*xx[1] + pp[2]*xx[2] + pp[3]*xx[3] :   0.0 :   True
    cc : Size=4, Index=A, Active=True
        Key : Lower : Body        : Upper : Active
          0 :   0.0 : pp[0]*xx[0] :   0.0 :   True
          1 :   0.0 : pp[1]*xx[1] :   0.0 :   True
          2 :   0.0 : pp[2]*xx[2] :   0.0 :   True
          3 :   0.0 : pp[3]*xx[3] :   0.0 :   True
    ccc : Size=5, Index=B, Active=True
        Key : Lower : Body                                                                          : Upper : Active
          0 :   0.0 : ppp[0,0]*xxx[0,0] + ppp[1,0]*xxx[1,0] + ppp[2,0]*xxx[2,0] + ppp[3,0]*xxx[3,0] :   0.0 :   True
          1 :   0.0 : ppp[0,1]*xxx[0,1] + ppp[1,1]*xxx[1,1] + ppp[2,1]*xxx[2,1] + ppp[3,1]*xxx[3,1] :   0.0 :   True
          2 :   0.0 : ppp[0,2]*xxx[0,2] + ppp[1,2]*xxx[1,2] + ppp[2,2]*xxx[2,2] + ppp[3,2]*xxx[3,2] :   0.0 :   True
          3 :   0.0 : ppp[0,3]*xxx[0,3] + ppp[1,3]*xxx[1,3] + ppp[2,3]*xxx[2,3] + ppp[3,3]*xxx[3,3] :   0.0 :   True
          4 :   0.0 : ppp[0,4]*xxx[0,4] + ppp[1,4]*xxx[1,4] + ppp[2,4]*xxx[2,4] + ppp[3,4]*xxx[3,4] :   0.0 :   True

12 Declarations: A B ppp pp p x xx xxx o c cc ccc
"""
    )


def test_simple1():
    model = models.simple1()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 Var Declarations
    x : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :   0.0 :  None :   1.0 : False :  True :  Reals
    y : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :   0.0 :  None :   1.0 : False :  True :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : x + y

3 Constraint Declarations
    c1 : Size=1, Index=None, Active=True
        Key  : Lower : Body  : Upper : Active
        None :   1.0 : x + y :   1.0 :   True
    c2 : Size=1, Index=None, Active=True
        Key  : Lower : Body    : Upper : Active
        None :  -Inf : 2*x + y :   1.0 :   True
    c3 : Size=1, Index=None, Active=True
        Key  : Lower : Body    : Upper : Active
        None :   1.0 : y - 2*x :  +Inf :   True

6 Declarations: x y o c1 c2 c3
"""
    )


def test_hs060():
    model = models.hs060()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """1 RangeSet Declarations
    N : Dimen=1, Size=4, Bounds=(1, 4)
        Key  : Finite : Members
        None :   True :   [1:4]

1 Var Declarations
    x : Size=4, Index=N
        Key : Lower : Value : Upper : Fixed : Stale : Domain
          1 :   -10 :   2.0 :    10 : False : False :  Reals
          2 :   -10 :   2.0 :    10 : False : False :  Reals
          3 :   -10 :   2.0 :    10 : False : False :  Reals
          4 :   -10 :   2.0 :    10 : False : False :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : (x[1] - 1)**2 + (x[1] - x[2])**2 + (x[2] - x[3])**4

1 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower             : Body                         : Upper             : Active
        None : 8.242640687119286 : x[1]*(1 + x[2]**2) + x[3]**4 : 8.242640687119286 :   True

4 Declarations: N x o c
"""
    )


def test_knapsack1():
    model = models.knapsack1()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """1 RangeSet Declarations
    INDEX : Dimen=1, Size=10, Bounds=(0, 9)
        Key  : Finite : Members
        None :   True :   [0:9]

2 Param Declarations
    v : Size=10, Index=INDEX, Domain=Reals, Default=None, Mutable=True
        Key : Value
          0 :     1
          1 :     1
          2 :     1
          3 :     1
          4 :     1
          5 :     1
          6 :     1
          7 :     1
          8 :     1
          9 :     1
    w : Size=10, Index=INDEX, Domain=Reals, Default=None, Mutable=True
        Key : Value
          0 :   1.0
          1 :   1.0
          2 :   1.0
          3 :   1.0
          4 :   1.0
          5 :   1.0
          6 :   1.0
          7 :   1.0
          8 :   1.0
          9 :   1.0

1 Var Declarations
    x : Size=10, Index=INDEX
        Key : Lower : Value : Upper : Fixed : Stale : Domain
          0 :   0.0 :  None :   1.0 : False :  True :  Reals
          1 :   0.0 :  None :   1.0 : False :  True :  Reals
          2 :   0.0 :  None :   1.0 : False :  True :  Reals
          3 :   0.0 :  None :   1.0 : False :  True :  Reals
          4 :   0.0 :  None :   1.0 : False :  True :  Reals
          5 :   0.0 :  None :   1.0 : False :  True :  Reals
          6 :   0.0 :  None :   1.0 : False :  True :  Reals
          7 :   0.0 :  None :   1.0 : False :  True :  Reals
          8 :   0.0 :  None :   1.0 : False :  True :  Reals
          9 :   0.0 :  None :   1.0 : False :  True :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : v[0]*x[0] + v[1]*x[1] + v[2]*x[2] + v[3]*x[3] + v[4]*x[4] + v[5]*x[5] + v[6]*x[6] + v[7]*x[7] + v[8]*x[8] + v[9]*x[9]

1 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body                                                                                                                  : Upper : Active
        None :  -Inf : w[0]*x[0] + w[1]*x[1] + w[2]*x[2] + w[3]*x[3] + w[4]*x[4] + w[5]*x[5] + w[6]*x[6] + w[7]*x[7] + w[8]*x[8] + w[9]*x[9] :   1.0 :   True

6 Declarations: INDEX w v x o c
"""
    )


def test_knapsack2():
    model = models.knapsack2()
    M = generate(model=model)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """1 RangeSet Declarations
    INDEX : Dimen=1, Size=10, Bounds=(0, 9)
        Key  : Finite : Members
        None :   True :   [0:9]

3 Param Declarations
    N : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :     1
    v : Size=10, Index=INDEX, Domain=Reals, Default=None, Mutable=True
        Key : Value
          0 :     1
          1 :     1
          2 :     1
          3 :     1
          4 :     1
          5 :     1
          6 :     1
          7 :     1
          8 :     1
          9 :     1
    w : Size=10, Index=INDEX, Domain=Reals, Default=None, Mutable=True
        Key : Value
          0 :   1.0
          1 :   1.0
          2 :   1.0
          3 :   1.0
          4 :   1.0
          5 :   1.0
          6 :   1.0
          7 :   1.0
          8 :   1.0
          9 :   1.0

1 Var Declarations
    x : Size=10, Index=INDEX
        Key : Lower : Value : Upper : Fixed : Stale : Domain
          0 :   0.0 :  None :   1.0 : False :  True :  Reals
          1 :   0.0 :  None :   1.0 : False :  True :  Reals
          2 :   0.0 :  None :   1.0 : False :  True :  Reals
          3 :   0.0 :  None :   1.0 : False :  True :  Reals
          4 :   0.0 :  None :   1.0 : False :  True :  Reals
          5 :   0.0 :  None :   1.0 : False :  True :  Reals
          6 :   0.0 :  None :   1.0 : False :  True :  Reals
          7 :   0.0 :  None :   1.0 : False :  True :  Reals
          8 :   0.0 :  None :   1.0 : False :  True :  Reals
          9 :   0.0 :  None :   1.0 : False :  True :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : v[0]*x[0] + v[1]*x[1] + v[2]*x[2] + v[3]*x[3] + v[4]*x[4] + v[5]*x[5] + v[6]*x[6] + v[7]*x[7] + v[8]*x[8] + v[9]*x[9]

1 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body                                                                                                                  : Upper     : Active
        None :  -Inf : w[0]*x[0] + w[1]*x[1] + w[2]*x[2] + w[3]*x[3] + w[4]*x[4] + w[5]*x[5] + w[6]*x[6] + w[7]*x[7] + w[8]*x[8] + w[9]*x[9] : N*10/10.0 :   True

7 Declarations: N INDEX w v x o c
"""
    )


def test_knapsack3():
    model = models.knapsack3()
    data = {"N": 1}
    M = generate(model=model, data=data)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """1 RangeSet Declarations
    INDEX : Dimen=1, Size=10, Bounds=(0, 9)
        Key  : Finite : Members
        None :   True :   [0:9]

3 Param Declarations
    N : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :     1
    v : Size=10, Index=INDEX, Domain=Reals, Default=None, Mutable=True
        Key : Value
          0 :     1
          1 :     1
          2 :     1
          3 :     1
          4 :     1
          5 :     1
          6 :     1
          7 :     1
          8 :     1
          9 :     1
    w : Size=10, Index=INDEX, Domain=Reals, Default=None, Mutable=True
        Key : Value
          0 :   1.0
          1 :   1.0
          2 :   1.0
          3 :   1.0
          4 :   1.0
          5 :   1.0
          6 :   1.0
          7 :   1.0
          8 :   1.0
          9 :   1.0

1 Var Declarations
    x : Size=10, Index=INDEX
        Key : Lower : Value : Upper : Fixed : Stale : Domain
          0 :   0.0 :  None :   1.0 : False :  True :  Reals
          1 :   0.0 :  None :   1.0 : False :  True :  Reals
          2 :   0.0 :  None :   1.0 : False :  True :  Reals
          3 :   0.0 :  None :   1.0 : False :  True :  Reals
          4 :   0.0 :  None :   1.0 : False :  True :  Reals
          5 :   0.0 :  None :   1.0 : False :  True :  Reals
          6 :   0.0 :  None :   1.0 : False :  True :  Reals
          7 :   0.0 :  None :   1.0 : False :  True :  Reals
          8 :   0.0 :  None :   1.0 : False :  True :  Reals
          9 :   0.0 :  None :   1.0 : False :  True :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : v[0]*x[0] + v[1]*x[1] + v[2]*x[2] + v[3]*x[3] + v[4]*x[4] + v[5]*x[5] + v[6]*x[6] + v[7]*x[7] + v[8]*x[8] + v[9]*x[9]

1 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body                                                                                                                  : Upper     : Active
        None :  -Inf : w[0]*x[0] + w[1]*x[1] + w[2]*x[2] + w[3]*x[3] + w[4]*x[4] + w[5]*x[5] + w[6]*x[6] + w[7]*x[7] + w[8]*x[8] + w[9]*x[9] : N*10/10.0 :   True

7 Declarations: N INDEX w v x o c
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
    M = generate(model=model, data=data)
    # M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """1 Set Declarations
    ITEMS : Size=1, Index=None, Ordered=Insertion
        Key  : Dimen : Domain : Size : Members
        None :     1 :    Any :    4 : {1, 2, 3, 4}

3 Param Declarations
    capacity : Size=1, Index=None, Domain=Reals, Default=None, Mutable=True
        Key  : Value
        None :    14
    value : Size=4, Index=ITEMS, Domain=Reals, Default=None, Mutable=True
        Key : Value
          1 :     8
          2 :     3
          3 :     6
          4 :    11
    weight : Size=4, Index=ITEMS, Domain=Reals, Default=None, Mutable=True
        Key : Value
          1 :     5
          2 :     7
          3 :     4
          4 :     3

1 Var Declarations
    x : Size=4, Index=ITEMS
        Key : Lower : Value : Upper : Fixed : Stale : Domain
          1 :   0.0 :  None :   1.0 : False :  True :  Reals
          2 :   0.0 :  None :   1.0 : False :  True :  Reals
          3 :   0.0 :  None :   1.0 : False :  True :  Reals
          4 :   0.0 :  None :   1.0 : False :  True :  Reals

1 Objective Declarations
    o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : value[1]*x[1] + value[2]*x[2] + value[3]*x[3] + value[4]*x[4]

1 Constraint Declarations
    c : Size=1, Index=None, Active=True
        Key  : Lower : Body                                                              : Upper    : Active
        None :  -Inf : weight[1]*x[1] + weight[2]*x[2] + weight[3]*x[3] + weight[4]*x[4] : capacity :   True

7 Declarations: ITEMS value weight capacity x o c
"""
    )

def test_pmedian1():
    model = models.pmedian1(5)
    M = generate(model=model)

    #M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 RangeSet Declarations
    M : Dimen=1, Size=5, Bounds=(0, 4)
        Key  : Finite : Members
        None :   True :   [0:4]
    N : Dimen=1, Size=5, Bounds=(0, 4)
        Key  : Finite : Members
        None :   True :   [0:4]

1 Param Declarations
    d : Size=25, Index=N*M, Domain=Reals, Default=None, Mutable=True
        Key    : Value
        (0, 0) :                2.0
        (0, 1) :                1.5
        (0, 2) : 1.3333333333333333
        (0, 3) :               1.25
        (0, 4) :                1.2
        (1, 0) :                1.5
        (1, 1) : 1.3333333333333333
        (1, 2) :               1.25
        (1, 3) :                1.2
        (1, 4) : 1.1666666666666667
        (2, 0) : 1.3333333333333333
        (2, 1) :               1.25
        (2, 2) :                1.2
        (2, 3) : 1.1666666666666667
        (2, 4) : 1.1428571428571428
        (3, 0) :               1.25
        (3, 1) :                1.2
        (3, 2) : 1.1666666666666667
        (3, 3) : 1.1428571428571428
        (3, 4) :              1.125
        (4, 0) :                1.2
        (4, 1) : 1.1666666666666667
        (4, 2) : 1.1428571428571428
        (4, 3) :              1.125
        (4, 4) : 1.1111111111111112

2 Var Declarations
    x : Size=25, Index=N*M
        Key    : Lower : Value : Upper : Fixed : Stale : Domain
        (0, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (0, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (0, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (0, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (0, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
    y : Size=5, Index=N
        Key : Lower : Value : Upper : Fixed : Stale : Domain
          0 :   0.0 :   0.0 :   1.0 : False : False : Binary
          1 :   0.0 :   0.0 :   1.0 : False : False : Binary
          2 :   0.0 :   0.0 :   1.0 : False : False : Binary
          3 :   0.0 :   0.0 :   1.0 : False : False : Binary
          4 :   0.0 :   0.0 :   1.0 : False : False : Binary

1 Objective Declarations
    _o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : d[0,0]*x[0,0] + d[0,1]*x[0,1] + d[0,2]*x[0,2] + d[0,3]*x[0,3] + d[0,4]*x[0,4] + d[1,0]*x[1,0] + d[1,1]*x[1,1] + d[1,2]*x[1,2] + d[1,3]*x[1,3] + d[1,4]*x[1,4] + d[2,0]*x[2,0] + d[2,1]*x[2,1] + d[2,2]*x[2,2] + d[2,3]*x[2,3] + d[2,4]*x[2,4] + d[3,0]*x[3,0] + d[3,1]*x[3,1] + d[3,2]*x[3,2] + d[3,3]*x[3,3] + d[3,4]*x[3,4] + d[4,0]*x[4,0] + d[4,1]*x[4,1] + d[4,2]*x[4,2] + d[4,3]*x[4,3] + d[4,4]*x[4,4]

3 Constraint Declarations
    bound_y : Size=25, Index=N*M, Active=True
        Key    : Lower : Body          : Upper : Active
        (0, 0) :  -Inf : x[0,0] - y[0] :   0.0 :   True
        (0, 1) :  -Inf : x[0,1] - y[0] :   0.0 :   True
        (0, 2) :  -Inf : x[0,2] - y[0] :   0.0 :   True
        (0, 3) :  -Inf : x[0,3] - y[0] :   0.0 :   True
        (0, 4) :  -Inf : x[0,4] - y[0] :   0.0 :   True
        (1, 0) :  -Inf : x[1,0] - y[1] :   0.0 :   True
        (1, 1) :  -Inf : x[1,1] - y[1] :   0.0 :   True
        (1, 2) :  -Inf : x[1,2] - y[1] :   0.0 :   True
        (1, 3) :  -Inf : x[1,3] - y[1] :   0.0 :   True
        (1, 4) :  -Inf : x[1,4] - y[1] :   0.0 :   True
        (2, 0) :  -Inf : x[2,0] - y[2] :   0.0 :   True
        (2, 1) :  -Inf : x[2,1] - y[2] :   0.0 :   True
        (2, 2) :  -Inf : x[2,2] - y[2] :   0.0 :   True
        (2, 3) :  -Inf : x[2,3] - y[2] :   0.0 :   True
        (2, 4) :  -Inf : x[2,4] - y[2] :   0.0 :   True
        (3, 0) :  -Inf : x[3,0] - y[3] :   0.0 :   True
        (3, 1) :  -Inf : x[3,1] - y[3] :   0.0 :   True
        (3, 2) :  -Inf : x[3,2] - y[3] :   0.0 :   True
        (3, 3) :  -Inf : x[3,3] - y[3] :   0.0 :   True
        (3, 4) :  -Inf : x[3,4] - y[3] :   0.0 :   True
        (4, 0) :  -Inf : x[4,0] - y[4] :   0.0 :   True
        (4, 1) :  -Inf : x[4,1] - y[4] :   0.0 :   True
        (4, 2) :  -Inf : x[4,2] - y[4] :   0.0 :   True
        (4, 3) :  -Inf : x[4,3] - y[4] :   0.0 :   True
        (4, 4) :  -Inf : x[4,4] - y[4] :   0.0 :   True
    num_facilities : Size=1, Index=None, Active=True
        Key  : Lower : Body                             : Upper : Active
        None :   1.0 : y[0] + y[1] + y[2] + y[3] + y[4] :   1.0 :   True
    single_x : Size=5, Index=M, Active=True
        Key : Lower : Body                                       : Upper : Active
          0 :   1.0 : x[0,0] + x[1,0] + x[2,0] + x[3,0] + x[4,0] :   1.0 :   True
          1 :   1.0 : x[0,1] + x[1,1] + x[2,1] + x[3,1] + x[4,1] :   1.0 :   True
          2 :   1.0 : x[0,2] + x[1,2] + x[2,2] + x[3,2] + x[4,2] :   1.0 :   True
          3 :   1.0 : x[0,3] + x[1,3] + x[2,3] + x[3,3] + x[4,3] :   1.0 :   True
          4 :   1.0 : x[0,4] + x[1,4] + x[2,4] + x[3,4] + x[4,4] :   1.0 :   True

9 Declarations: N M d x y _o single_x bound_y num_facilities
"""
    )



def test_pmedian2():
    model = models.pmedian2(5)
    M = generate(model=model)

    #M.pprint()
    out = StringIO()
    M.pprint(ostream=out)
    assert (
        out.getvalue()
        == """2 RangeSet Declarations
    M : Dimen=1, Size=5, Bounds=(0, 4)
        Key  : Finite : Members
        None :   True :   [0:4]
    N : Dimen=1, Size=5, Bounds=(0, 4)
        Key  : Finite : Members
        None :   True :   [0:4]

1 Param Declarations
    d : Size=25, Index=N*M, Domain=Reals, Default=None, Mutable=False
        Key    : Value
        (0, 0) :                2.0
        (0, 1) :                1.5
        (0, 2) : 1.3333333333333333
        (0, 3) :               1.25
        (0, 4) :                1.2
        (1, 0) :                1.5
        (1, 1) : 1.3333333333333333
        (1, 2) :               1.25
        (1, 3) :                1.2
        (1, 4) : 1.1666666666666667
        (2, 0) : 1.3333333333333333
        (2, 1) :               1.25
        (2, 2) :                1.2
        (2, 3) : 1.1666666666666667
        (2, 4) : 1.1428571428571428
        (3, 0) :               1.25
        (3, 1) :                1.2
        (3, 2) : 1.1666666666666667
        (3, 3) : 1.1428571428571428
        (3, 4) :              1.125
        (4, 0) :                1.2
        (4, 1) : 1.1666666666666667
        (4, 2) : 1.1428571428571428
        (4, 3) :              1.125
        (4, 4) : 1.1111111111111112

2 Var Declarations
    x : Size=25, Index=N*M
        Key    : Lower : Value : Upper : Fixed : Stale : Domain
        (0, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (0, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (0, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (0, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (0, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (1, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (2, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (3, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 0) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 1) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 2) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 3) :   0.0 :   0.0 :   1.0 : False : False : Binary
        (4, 4) :   0.0 :   0.0 :   1.0 : False : False : Binary
    y : Size=5, Index=N
        Key : Lower : Value : Upper : Fixed : Stale : Domain
          0 :   0.0 :   0.0 :   1.0 : False : False : Binary
          1 :   0.0 :   0.0 :   1.0 : False : False : Binary
          2 :   0.0 :   0.0 :   1.0 : False : False : Binary
          3 :   0.0 :   0.0 :   1.0 : False : False : Binary
          4 :   0.0 :   0.0 :   1.0 : False : False : Binary

1 Objective Declarations
    _o : Size=1, Index=None, Active=True
        Key  : Active : Sense    : Expression
        None :   True : minimize : 2.0*x[0,0] + 1.5*x[0,1] + 1.3333333333333333*x[0,2] + 1.25*x[0,3] + 1.2*x[0,4] + 1.5*x[1,0] + 1.3333333333333333*x[1,1] + 1.25*x[1,2] + 1.2*x[1,3] + 1.1666666666666667*x[1,4] + 1.3333333333333333*x[2,0] + 1.25*x[2,1] + 1.2*x[2,2] + 1.1666666666666667*x[2,3] + 1.1428571428571428*x[2,4] + 1.25*x[3,0] + 1.2*x[3,1] + 1.1666666666666667*x[3,2] + 1.1428571428571428*x[3,3] + 1.125*x[3,4] + 1.2*x[4,0] + 1.1666666666666667*x[4,1] + 1.1428571428571428*x[4,2] + 1.125*x[4,3] + 1.1111111111111112*x[4,4]

3 Constraint Declarations
    bound_y : Size=25, Index=N*M, Active=True
        Key    : Lower : Body          : Upper : Active
        (0, 0) :  -Inf : x[0,0] - y[0] :   0.0 :   True
        (0, 1) :  -Inf : x[0,1] - y[0] :   0.0 :   True
        (0, 2) :  -Inf : x[0,2] - y[0] :   0.0 :   True
        (0, 3) :  -Inf : x[0,3] - y[0] :   0.0 :   True
        (0, 4) :  -Inf : x[0,4] - y[0] :   0.0 :   True
        (1, 0) :  -Inf : x[1,0] - y[1] :   0.0 :   True
        (1, 1) :  -Inf : x[1,1] - y[1] :   0.0 :   True
        (1, 2) :  -Inf : x[1,2] - y[1] :   0.0 :   True
        (1, 3) :  -Inf : x[1,3] - y[1] :   0.0 :   True
        (1, 4) :  -Inf : x[1,4] - y[1] :   0.0 :   True
        (2, 0) :  -Inf : x[2,0] - y[2] :   0.0 :   True
        (2, 1) :  -Inf : x[2,1] - y[2] :   0.0 :   True
        (2, 2) :  -Inf : x[2,2] - y[2] :   0.0 :   True
        (2, 3) :  -Inf : x[2,3] - y[2] :   0.0 :   True
        (2, 4) :  -Inf : x[2,4] - y[2] :   0.0 :   True
        (3, 0) :  -Inf : x[3,0] - y[3] :   0.0 :   True
        (3, 1) :  -Inf : x[3,1] - y[3] :   0.0 :   True
        (3, 2) :  -Inf : x[3,2] - y[3] :   0.0 :   True
        (3, 3) :  -Inf : x[3,3] - y[3] :   0.0 :   True
        (3, 4) :  -Inf : x[3,4] - y[3] :   0.0 :   True
        (4, 0) :  -Inf : x[4,0] - y[4] :   0.0 :   True
        (4, 1) :  -Inf : x[4,1] - y[4] :   0.0 :   True
        (4, 2) :  -Inf : x[4,2] - y[4] :   0.0 :   True
        (4, 3) :  -Inf : x[4,3] - y[4] :   0.0 :   True
        (4, 4) :  -Inf : x[4,4] - y[4] :   0.0 :   True
    num_facilities : Size=1, Index=None, Active=True
        Key  : Lower : Body                             : Upper : Active
        None :   1.0 : y[0] + y[1] + y[2] + y[3] + y[4] :   1.0 :   True
    single_x : Size=5, Index=M, Active=True
        Key : Lower : Body                                       : Upper : Active
          0 :   1.0 : x[0,0] + x[1,0] + x[2,0] + x[3,0] + x[4,0] :   1.0 :   True
          1 :   1.0 : x[0,1] + x[1,1] + x[2,1] + x[3,1] + x[4,1] :   1.0 :   True
          2 :   1.0 : x[0,2] + x[1,2] + x[2,2] + x[3,2] + x[4,2] :   1.0 :   True
          3 :   1.0 : x[0,3] + x[1,3] + x[2,3] + x[3,3] + x[4,3] :   1.0 :   True
          4 :   1.0 : x[0,4] + x[1,4] + x[2,4] + x[3,4] + x[4,4] :   1.0 :   True

9 Declarations: N M d x y _o single_x bound_y num_facilities
"""
    )


