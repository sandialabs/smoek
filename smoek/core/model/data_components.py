from smoek.core.expr.nodes import ExprLeaf, _wrap_expression_if_needed
from .components import ModelingComponent, index


# Mutable model data
class Parameter(ModelingComponent, ExprLeaf):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)
        self._value = None

    def value(self, value=None):
        if value is None:
            return self._value
        self._value = _wrap_expression_if_needed(value)
        return self

    def index_set(self, iset):
        return self.forall(index(f"i{len(self._index_sets())}") in iset, explicit=False)


def parameter(name=None, doc=None):
    return Parameter(name=name, doc=doc)


# Constant model data
class Data(ModelingComponent, ExprLeaf):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)

    def value(self, value=None):
        if value is None:
            return self._value
        self._value = _wrap_expression_if_needed(value)
        return self

    def index_set(self, iset):
        return self.forall(index(f"i{len(self._index_sets())}") in iset, explicit=False)


def data(name=None, doc=None):
    return Data(name=name, doc=doc)
