from enum import Enum
from .components import ModelingComponent
from .expr_components import ExprLeaf, ComponentIndicesNode

class Domain(Enum):
    Reals = 1
    Binary = 2

# TODO: I don't think we need to differentiate between ScalarVariable and IndexedVariable
# Calling variable().forall(...) will automatically create an indexed variable
# However, scalar vars need to inherit Expr Leaf while indexed need __getitem__ method
class ScalarVariable(ModelingComponent, ExprLeaf):
    def __init__(self, name=None, domain=None, doc=None):
        super().__init__(name, doc)
        if domain is not None:
            assert isinstance(domain, Domain)
        self._domain = domain

def variable(name=None, domain=Domain.Reals, doc=None, forall=None):
    if forall is None:
        return ScalarVariable(name=name, domain=domain, doc=doc)
    else:
        return IndexedVariable(forall, name=name, domain=domain, doc=doc)


def binary_variable(name=None, doc=None):
    return ScalarVariable(name=name, domain=Domain.Binary, doc=doc)

def real_variable(name=None, doc=None):
    return ScalarVariable(name=name, domain=Domain.Reals, doc=doc)


class IndexedVariable(ModelingComponent):
    def __init__(self, forall, name=None, domain=None, doc=None):
        super().__init__(name, doc)
        if domain is not None:
            assert isinstance(domain, Domain)
        self._domain = domain
        self._forall = forall

    def __getitem__(self, indices):
        return ComponentIndicesNode(self, indices)