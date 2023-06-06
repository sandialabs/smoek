from smoek.core import variable
import pytest

#
# Single variables
#

def test_single_var_name():
    v = variable()
    with pytest.raises(AssertionError, match="No name specified for this variable"):
        v.name
    v.name = "x"
    assert v.name == "x"

def test_single_var_value():
    v = variable(value=2)
    assert v.value == 2
    v.value = 3
    assert v.value == 3

#
# Indexed variables
#

def test_indexed_var_name():
    #
    # Creating an array of variables
    #
    v = variable(5)
    #
    # No name was specified for the array
    #
    with pytest.raises(AssertionError, match="No name specified for this variable"):
        v.name
    with pytest.raises(AssertionError, match="No name specified for this variable"):
        v[0].name
    #
    # Specify the name for the array
    #
    v.name = "x"
    assert v.name == "x"
    assert v[0].name == "x[0]"
    #
    # Creating an array of variables with a name
    #
    v = variable(5, name="y")
    assert v.name == "y"
    assert v[0].name == "y[0]"

def test_indexed_var_value():
    #
    # Creating an array of variables
    #
    v = variable(5, value=0)
    assert v.value == 0
    #
    # The values of v[0] and v[1] are set with the initializing value
    #
    assert v[0].value == 0
    assert v[1].value == 0
    #
    # We reset the value of v[0]
    #
    v[0].value = 1
    assert v.value == 0
    assert v[0].value == 1
    assert v[1].value == 0
    #
    # We specify the value for an array of variables.  We do *not* treat this as a concrete model.  Rather, we set
    #       the value of all of the indexed variables that have already been referenced.
    #
    v.value = 2
    assert v.value == 2
    assert v[0].value == 2
    assert v[1].value == 2

