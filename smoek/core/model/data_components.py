from smoek.core.expr.nodes import ExprLeaf
from .components import ModelingComponent


# Mutable model data
class Parameter(ModelingComponent, ExprLeaf):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)


def parameter(name=None, doc=None):
    return Parameter(name=name, doc=doc)


# Constant model data
class Data(ModelingComponent, ExprLeaf):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)


def data(name=None, doc=None):
    return Data(name=name, doc=doc)
