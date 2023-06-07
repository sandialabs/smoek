import re
import pytest
from smoek.core import variable, parameter


def test_mul_error1():
    class TMP(object):
        pass

    a = variable(name="a")
    with pytest.raises(TypeError, match=re.escape("unsupported operand type(s) for *: 'TMP' and 'SingleVariable'")):
        TMP() * a

def test_mul_error2():
    #
    # ERROR HERE?
    #
    v = variable(10)
    s = variable()

    v * s

def test_mul_simple():
    a = variable(name="a")
    b = variable(name="b")

    e = a*b
    assert e.to_list() == ["*", "a", "b"]

    e = a
    e *= b
    assert e.to_list() == ["*", "a", "b"]

def test_mul_const():
    a = variable(name="a")

    e = 5*a
    assert e.to_list() == ["*", "5", "a"]

    e = a*5
    assert e.to_list() == ["*", "a", "5"]

    e = 5.0*a
    assert e.to_list() == ["*", "5.0", "a"]

    e = a*5.0
    assert e.to_list() == ["*", "a", "5.0"]

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
    assert e.to_list() == ["*", ["*", "a", "b"], "5"]

    #       *
    #      / \
    #     5   *
    #        / \
    #       a   b
    e1 = a * b
    e = 5 * e1
    #
    assert e.to_list() == ["*", "5", ["*", "a", "b"]]

    #           *
    #          / \
    #         *   c
    #        / \
    #       a   b
    e1 = a * b
    e = e1 * c
    #
    assert e.to_list() == ["*", ["*", "a", "b"], "c"]

    #       *
    #      / \
    #     c   *
    #        / \
    #       a   b
    e1 = a * b
    e = c * e1
    #
    assert e.to_list() == ["*", "c", ["*", "a", "b"]]

    #            *
    #          /   \
    #         *     *
    #        / \   / \
    #       a   b c   d
    e1 = a * b
    e2 = c * d
    e = e1 * e2
    #
    assert e.to_list() == ["*", ["*", "a", "b"], ["*", "c", "d"]]

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
    assert e.to_list() == ["*", ["+", "c", ["+", "a", "b"]], ["+", ["+", "a", "b"], "d"]]

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
    assert e.to_list() == ["*", ["*", "c", ["+", "a", "b"]], ["*", ["+", "a", "b"], "d"]]

def test_mul_trivial_1():
    #
    # Check that multiplying by one doesn't change the expression
    #
    a = variable(name="a")

    e = a * 1
    assert e.to_list() == "a"

    e = 1 * a
    assert e.to_list() == "a"

    e = a * 1.0
    assert e.to_list() == "a"

    e = 1.0 * a
    assert e.to_list() == "a"

    e = a
    e *= 1
    assert e.to_list() == "a"

    e = a
    e *= 1.0
    assert e.to_list() == "a"

    #
    # Multiplying by one will not change the expression
    #
    e = a + a
    f = e * 1
    assert f.to_list() == ["+", "a", "a"]

def test_mul_trivial_0():
    #
    # Check that multiplying by zero gives zero
    #
    a = variable(name="a")

    e = a * 0
    assert e.to_list() == "0"

    e = 0 * a
    assert e.to_list() == "0"

    e = a * 0.0
    assert e.to_list() == "0"

    e = 0.0 * a
    assert e.to_list() == "0"

    e = a
    e *= 0
    assert e.to_list() == "0"

    e = a
    e *= 0.0
    assert e.to_list() == "0"

    #
    # Multiplying by zero gives zero
    #
    e = a + a
    f = e * 0
    assert f.to_list() == "0"

