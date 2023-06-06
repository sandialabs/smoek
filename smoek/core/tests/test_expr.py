import re
import pytest
from smoek.core import variable, parameter


def test_sum_error1():
    class TMP(object):
        pass

    a = variable(name="a")
    TMP() + a
    with pytest.raises(TypeError, match=re.escape("unsupported operand type(s) for +: 'TMP' and 'SingleVariable'")):
        TMP() + a

def test_sum_error2():
    #
    # ERROR HERE?
    #
    v = variable(10)
    s = variable()

    v + s

def test_sum_simple():
    a = variable(name="a")
    b = variable(name="b")

    e = a+b
    assert e.to_list() == ["+", "a", "b"]

def test_sum_nested():
    a = variable(name="a")
    b = variable(name="b")
    c = variable(name="c")
    d = variable(name="d")

    #           +
    #          / \
    #         +   5
    #        / \
    #       a   b
    e1 = a + b
    e = e1 + 5
    #
    assert e.to_list() == ["+", ["+", "a", "b"], "5"]

    #       +
    #      / \
    #     5   +
    #        / \
    #       a   b
    e1 = a + b
    e = 5 + e1
    #
    assert e.to_list() == ["+", "5", ["+", "a", "b"]]

    #           +
    #          / \
    #         +   c
    #        / \
    #       a   b
    e1 = a + b
    e = e1 + c
    #
    assert e.to_list() == ["+", ["+", "a", "b"], "c"]

    #       +
    #      / \
    #     c   +
    #        / \
    #       a   b
    e1 = a + b
    e = c + e1
    #
    assert e.to_list() == ["+", "c", ["+", "a", "b"]]

    #            +
    #          /   \
    #         +     +
    #        / \   / \
    #       a   b c   d
    e1 = a + b
    e2 = c + d
    e = e1 + e2
    #
    assert e.to_list() == ["+", ["+", "a", "b"], ["+", "c", "d"]]

def test_sum_const():
    a = variable(name="a")

    e = 5+a
    assert e.to_list() == ["+", "5", "a"]

    e = a+5
    assert e.to_list() == ["+", "a", "5"]

    e = 5.0+a
    assert e.to_list() == ["+", "5.0", "a"]

    e = a+5.0
    assert e.to_list() == ["+", "a", "5.0"]


