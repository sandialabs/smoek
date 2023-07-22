import math
import pytest
from smoek.core import index, index_set, forall
from smoek.core.components import ComponentIndicesNode
from smoek.core.set_components import Index, ScalarSet, IndexedSet
#
# Scalar index set
#
def test_index_function():
    i = index()
    assert type(i) == Index

def test_index_set_function():
    I = index_set()
    assert type(I) == ScalarSet

    i = index('i')
    I = index_set('I')
    f = forall(i, In=I)

    II = index_set('II', forall=f)
    assert type(II) == IndexedSet
    
def test_index():
    i = index()
    with pytest.raises(AssertionError, match="No name specified for this component"):
        i.name
    i.name = 'i'
    assert i.name == 'i'

    i = index('i')
    assert i.name == 'i'

    # test to_string
    assert str(i) == 'i'


def test_scalar_set():
    s = index_set()
    with pytest.raises(AssertionError, match="No name specified for this component"):
        s.name
    s.name = "A"
    assert s.name == "A"

    s = index_set('A')
    assert s.name == "A"

    # test to_string
    assert str(s) == 'A'

def test_indexed_set():
    i = index('i')
    I = index_set('I')
    f = forall(i, In=I)

    s = index_set(forall=f)
    assert s._forall is f
    si = s[i]
    assert type(si) is ComponentIndicesNode
    assert si._component is s
    assert si._indices is i

    with pytest.raises(AssertionError, match="No name specified for this component"):
        s.name
    s.name = "A"
    assert s.name == "A"


    s = index_set('A')
    assert s.name == "A"

    # test to_string
    assert str(s) == 'A'
    
