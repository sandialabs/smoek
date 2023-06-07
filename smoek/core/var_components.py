import math

from .components import IndexableComponent
from .expression import ExprLeaf, VariableIndexExpression


class IndexedVariable(IndexableComponent):
    def __init__(self, name=None):
        super().__init__(name)
        self._value = math.nan
                
    @property
    def name(self):
        assert self._name is not None, "No name specified for this variable"
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    def __getitem__(self, indices):
        tmp = self._used_indices.get(indices, None)
        if tmp is not None:
            return tmp
        tmp = VariableIndexExpression(self, indices)
        self._used_indices[indices] = tmp
        return tmp

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        for var in self._used_indices.values():
            var._value = v

class SingleVariable(ExprLeaf):
    def __init__(self, name=None):
        super().__init__()
        self._name = name
        self._value = math.nan

    @property
    def name(self):
        assert self._name is not None, "No name specified for this variable"
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    def to_string(self):
        return self.name

def variable(index=None, *, name=None, value=None):
    if index is None:
        v = SingleVariable(name=name)
        if value is not None:
            v.value = value
        return v
    else:
        # TODO: Configure the index dimensions "args[0]"
        v = IndexedVariable(name=name)
        if value is not None:
            v.value = value
        return v

