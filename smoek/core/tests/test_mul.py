import re
import pytest
from smoek.core import variable, parameter, index, index_set, forall
from smoek.core.utils import expr_to_list


def test_mul_errors():
    # unknown types
    class TMP(object):
        pass

    a = variable(name="a")
    with pytest.raises(TypeError) as excinfo:
        TMP()*a
    assert str(excinfo.value).startswith('unsupported operand type(s) in expression')
    with pytest.raises(TypeError) as excinfo:
        a*TMP()
    assert str(excinfo.value).startswith('unsupported operand type(s) in expression')

    i = index('i')
    I = index_set('I')
    v = variable(forall=forall(i, In=I))
    s = variable()
    with pytest.raises(TypeError) as excinfo:
        foo = v*s
    assert str(excinfo.value).startswith('unsupported operand type(s) in expression')
    with pytest.raises(TypeError) as excinfo:
        foo = s*v
    assert str(excinfo.value).startswith('unsupported operand type(s) in expression')

def test_mul_variables():
    a = variable(name="a")
    b = variable(name="b")

    e = a*b
    assert expr_to_list(e) == ["*", "a", "b"]

    e = a
    e *= b
    assert expr_to_list(e) == ["*", "a", "b"]

def test_mul_const():
    a = variable(name="a")

    e = 5*a
    assert expr_to_list(e) == ["*", "5", "a"]

    e = a*5
    assert expr_to_list(e) == ["*", "a", "5"]

    e = 5.0*a
    assert expr_to_list(e) == ["*", "5.0", "a"]

    e = a*5.0
    assert expr_to_list(e)== ["*", "a", "5.0"]

def test_mul_nested():
    a = variable(name="a")
    b = variable(name="b")
    c = variable(name="c")
    d = variable(name="d")

    #           *
    #          / \
    #         *   5
    #        / \
    #       a   b
    e1 = a * b
    e = e1 * 5
    #
    assert expr_to_list(e) == ["*", ["*", "a", "b"], "5"]

    #       *
    #      / \
    #     5   *
    #        / \
    #       a   b
    e1 = a * b
    e = 5 * e1
    #
    assert expr_to_list(e) == ["*", "5", ["*", "a", "b"]]

    #           *
    #          / \
    #         *   c
    #        / \
    #       a   b
    e1 = a * b
    e = e1 * c
    #
    assert expr_to_list(e) == ["*", ["*", "a", "b"], "c"]

    #       *
    #      / \
    #     c   *
    #        / \
    #       a   b
    e1 = a * b
    e = c * e1
    #
    assert expr_to_list(e) == ["*", "c", ["*", "a", "b"]]

    #            *
    #          /   \
    #         *     *
    #        / \   / \
    #       a   b c   d
    e1 = a * b
    e2 = c * d
    e = e1 * e2
    #
    assert expr_to_list(e) == ["*", ["*", "a", "b"], ["*", "c", "d"]]

    #
    # Check the structure of nested products
    #
    #            *
    #          /   \
    #         +     +
    #        / \   / \
    #       c    +    d
    #           / \
    #          a   b
    e1 = a + b
    e2 = c + e1
    e3 = e1 + d
    e = e2 * e3
    assert expr_to_list(e) == ["*", ["+", "c", ["+", "a", "b"]], ["+", ["+", "a", "b"], "d"]]

    #
    # Check the structure of nested products
    #
    #            *
    #          /   \
    #         *     *
    #        / \   / \
    #       c    +    d
    #           / \
    #          a   b
    e1 = a + b
    e2 = c * e1
    e3 = e1 * d
    e = e2 * e3
    assert expr_to_list(e) == ["*", ["*", "c", ["+", "a", "b"]], ["*", ["+", "a", "b"], "d"]]

def test_mul_trivial_1():
    #
    # Check that multiplying by one doesn't change the expression
    #
    a = variable(name="a")

    e = a * 1
    assert expr_to_list(e) == "a"

    e = 1 * a
    assert expr_to_list(e)== "a"

    e = a * 1.0
    assert expr_to_list(e) == "a"

    e = 1.0 * a
    assert expr_to_list(e) == "a"

    e = a
    e *= 1
    assert expr_to_list(e) == "a"

    e = a
    e *= 1.0
    assert expr_to_list(e) == "a"

    #
    # Multiplying by one will not change the expression
    #
    e = a + a
    f = e * 1
    assert expr_to_list(e) == ["+", "a", "a"]

def test_mul_trivial_0():
    #
    # Check that multiplying by zero gives zero
    #
    a = variable(name="a")

    e = a * 0
    assert expr_to_list(e) == "0"

    e = 0 * a
    assert expr_to_list(e) == "0"

    e = a * 0.0
    assert expr_to_list(e) == "0.0"

    e = 0.0 * a
    assert expr_to_list(e) == "0.0"

    e = a
    e *= 0
    assert expr_to_list(e) == "0"

    e = a
    e *= 0.0
    assert expr_to_list(e) == "0.0"

    #
    # Multiplying by zero gives zero
    #
    e = a + a
    f = e * 0
    assert expr_to_list(f) == "0"


if __name__ == "__main__":
    test_mul_errors()
    test_mul_variables()
    test_mul_const()
    test_mul_nested()
    test_mul_trivial_1()
    test_mul_trivial_0()