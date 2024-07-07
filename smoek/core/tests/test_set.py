import pytest
import math
from smoek import index, index_set
from smoek.core.expr.forall import forall
from smoek.core.expr.nodes import ComponentIndicesNode
from smoek.core.model.components import Index
from smoek.core.model.set_components import Set


#
# Scalar index set
#
def test_index_function():
    i = index()
    assert type(i) == Index


def test_index_set_function():
    I = index_set()
    assert type(I) == Set
    assert not I.is_indexed()

    i = index("i")
    I = index_set("I")
    f = forall(i, In=I)
    II = index_set("II", forall=f)
    assert type(II) == Set
    assert II.is_indexed()


def test_index():
    i = index()
    with pytest.raises(AssertionError, match="No name specified for this component"):
        i.name()
    i.name("i")
    assert i.name() == "i"

    i = index("i")
    assert i.name() == "i"

    # test to_string
    assert str(i) == "i"


def test_scalar_set():
    s = index_set()
    with pytest.raises(AssertionError, match="No name specified for this component"):
        s.name()
    s.name("A")
    assert s.name() == "A"

    s = index_set("A")
    assert s.name() == "A"

    # test to_string
    assert str(s) == "A"


def test_indexed_set():
    i = index("i")
    I = index_set("I")
    f = forall(i, In=I)
    s = index_set(forall=f)
    assert s._forall is f

    si = s[i]
    assert type(si) is ComponentIndicesNode
    assert si._component is s
    # TODO: determine whether this is intended behavior
    assert si._indices[0] is i

    with pytest.raises(AssertionError, match="No name specified for this component"):
        s.name()
    s.name("A")
    assert s.name() == "A"

    s = index_set("A")
    assert s.name() == "A"

    # test to_string
    assert str(s) == "A"


def test_multi_indexed_set():
    i = index("i")
    I = index_set("I")
    j = index("j")
    J = index_set("J")
    s = index_set().forall(i, In=I).forall(j, In=J)
    sij = s[i, j]
    assert type(sij) is ComponentIndicesNode
    assert sij._component is s
    assert sij._indices[0] is i
    assert sij._indices[1] is j
