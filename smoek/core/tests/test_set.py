import math
import pytest
from smoek.core import index_set

#
# Single index set
#

def test_single_set_name():
    s = index_set()
    with pytest.raises(AssertionError, match="No name specified for this set"):
        s.name
    s.name = "A"
    assert s.name == "A"

def test_single_set_elements():
    s = index_set()
    assert s.elements == []
    s.elements = [7,9,11]
    assert s.elements == [7,9,11]

def test_single_set_default_elements():
    s = index_set()
    assert s.elements == []

#
# Indexed sets
#

def test_indexed_set_name():
    #
    # Creating an array of index sets
    #
    s = index_set(5)
    #
    # No name was specified for the array
    #
    with pytest.raises(AssertionError, match="No name specified for this set"):
        s.name
    with pytest.raises(AssertionError, match="No name specified for this set"):
        s[0].name
    #
    # Specify the name for the array
    #
    s.name = "x"
    assert s.name == "x"
    assert s[0].name == "x[0]"
    #
    # Creating an array of sets with a name
    #
    s = index_set(5, "y")
    assert s.name == "y"
    assert s[0].name == "y[0]"

def test_indexed_set_elements():
    #
    # Creating an array of sets
    #
    s = index_set(5)
    s.elements = [1,3,5]
    assert s.elements == [1,3,5]
    #
    # The elements of s[0] and s[1] are set with the initial elements
    #
    assert s[0].elements == [1,3,5]
    assert s[1].elements == [1,3,5]
    #
    # We reset the elements of s[0]
    #
    s[0].elements = [7,9,11]
    assert s.elements == [1,3,5]
    assert s[0].elements == [7,9,11]
    assert s[1].elements == [1,3,5]
    #
    # We specify the elements for an array of sets.  We do *not* treat this as a concrete model.  Rather, we set
    #       the elements of all of the indexed sets that have already been referenced.
    #
    s.elements = [13,15,17]
    assert s.elements == [13,15,17]
    assert s[0].elements == [13,15,17]
    assert s[1].elements == [13,15,17]

def test_indexed_set_default_elements():
    s = index_set(3)
    assert s[0].elements == []

