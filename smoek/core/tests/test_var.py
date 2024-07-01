import pytest
import math
from smoek.core import variable, forall, index, index_set
from smoek.core.components import ComponentIndicesNode
from smoek.core.var_components import IndexedVariable, ScalarVariable


def test_variable_function():
    v = variable()
    assert type(v) is ScalarVariable

    i = index("i")
    I = index_set("I")
    f = forall(i, In=I)

    v = variable(forall=f)
    assert type(v) is IndexedVariable


def test_scalar_var():
    # test name
    v = variable()
    with pytest.raises(AssertionError, match="No name specified for this component"):
        v.name
    v.name = "x"
    assert v.name == "x"

    v = variable("x")
    assert v.name == "x"

    # test to_string
    assert str(v) == "x"


# WEH - What is this test for?
@pytest.mark.skip("TODO: finish this one")
def test_scalar_var_in_expression():
    pass


def test_indexed_var():
    i = index("i")
    I = index_set("I")
    f = forall(i, In=I)

    # test name
    v = variable(forall=f)
    with pytest.raises(AssertionError, match="No name specified for this component"):
        v.name
    v.name = "x"
    assert v.name == "x"

    assert v._forall is f
    vi = v[i]
    assert type(vi) is ComponentIndicesNode
    assert vi._component is v
    # TODO: determine whether this is intended behavior
    assert vi._indices[0] is i

    v = variable("x", forall=f)
    assert v.name == "x"

    # test to_string
    assert str(v) == "x"
