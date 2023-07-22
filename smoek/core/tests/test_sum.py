import re
import pytest
from smoek.core import variable, index, index_set, forall


def test_sum_errors():
    # unknown types
    class TMP(object):
        pass

    a = variable(name="a")
    with pytest.raises(TypeError) as excinfo:
        TMP() + a
    assert str(excinfo.value).startswith('unsupported operand type(s) in expression')
    with pytest.raises(TypeError) as excinfo:
        a + TMP()
    assert str(excinfo.value).startswith('unsupported operand type(s) in expression')

    # IndexedVariable with no index
    # TODO: We should have special error for this case - it is likely common
    i = index('i')
    I = index_set('I')
    v = variable(forall=forall(i, In=I))
    s = variable()
    with pytest.raises(TypeError) as excinfo:
        foo = v + s
    assert str(excinfo.value).startswith('unsupported operand type(s) in expression')
    with pytest.raises(TypeError) as excinfo:
        foo = s + v
    assert str(excinfo.value).startswith('unsupported operand type(s) in expression')

def test_sum_variables():
    a = variable(name="a")
    b = variable(name="b")

    e = a+b
    assert e.to_list() == ["+", "a", "b"]

    e = a
    e += b
    assert e.to_list() == ["+", "a", "b"]

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

    #           +
    #          / \
    #         *   c
    #        / \
    #       2   +
    #          / \
    #         a   b
    e1 = a + b
    e = 2 * e1 + c
    #
    assert e.to_list() == ["+", ["*", "2", ["+", "a", "b"]], "c"]

    #         *
    #        / \
    #       3   +
    #          / \
    #         *   c
    #        / \
    #       2   +
    #          / \
    #         a   b
    e1 = a + b
    e = 3 * (2 * e1 + c)
    #
    assert e.to_list() == ["*", "3", ["+", ["*", "2", ["+", "a", "b"]], "c"]]

    #       +
    #      / \
    #     *   b
    #    / \
    #   a   5
    e1 = a * 5
    e = e1 + b
    #
    assert e.to_list() == ["+", ["*", "a", "5"], "b"]

    #       +
    #      / \
    #     b   *
    #        / \
    #       a   5
    e1 = a * 5
    e = b + e1
    #
    assert e.to_list() == ["+", "b", ["*", "a", "5"]]

    #            +
    #          /   \
    #         *     +
    #        / \   / \
    #       a   5 b   c
    e1 = a * 5
    e2 = b + c
    e = e1 + e2
    #
    assert e.to_list() == ["+", ["*", "a", "5"], ["+", "b", "c"]]

    #            +
    #          /   \
    #         +     *
    #        / \   / \
    #       b   c a   5
    e2 = b + c
    e = e2 + e1
    #
    assert e.to_list() == ["+", ["+", "b", "c"], ["*", "a", "5"]]

def test_sum_trivial():
    #
    # Check that adding zero doesn't change the expression
    #
    a = variable(name="a")

    e = a + 0
    assert e.to_list() == "a"

    e = 0 + a
    assert e.to_list() == "a"

    e = a + 0.0
    assert e.to_list() == "a"

    e = 0.0 + a
    assert e.to_list() == "a"

    e = a
    e += 0
    assert e.to_list() == "a"

    e = a
    e += 0.0
    assert e.to_list() == "a"

    #
    # Adding zero to a sum will not change the sum
    #
    e = a + a
    f = e + 0
    assert f.to_list() == ["+", "a", "a"]

