from enum import Enum
from .components import ModelingComponent
from .expression import ExprLeaf

class Domain(Enum):
    Reals = 1
    Binary = 2

class Variable(ModelingComponent, ExprLeaf):
    def __init__(self, name=None, domain=None, doc=None):
        super().__init__(name, doc)
        if domain is not None:
            assert isinstance(domain, Domain)
        self._domain = domain

def variable(name=None, domain=None, doc=None):
    return Variable(name=name, domain=domain, doc=doc)

def binary_variable(name=None, doc=None):
    return Variable(name=name, domain=Domain.Binary, doc=doc)

def real_variable(name=None, doc=None):
    return Variable(name=name, domain=Domain.Reals, doc=doc)

"""                
class ScalarVariable(ScalarComponent, ExprLeaf):
    def __init__(self, name=None, domain=None, doc=None):
        super().__init__(name=name, doc=doc)
        if domain is not None:
            assert isinstance(domain, Domain)
        self._domain = domain

    @property
    def domain(self):
        return self._domain

    def to_string(self):
        return self.name

# Todo: think about having a single object that has a forall
# or doesn't have a forall to differentiate scalar vs indexed?
class IndexedVariable(IndexedComponent):
    def __init__(self, name=None, domain=None, forall=None, doc=None):
        super().__init__(name=name, forall=forall, doc=doc)
        self._domain = domain

    @property
    def domain(self):
        return self._domain

def _variable(name=None, domain=None, forall=None, doc=None):
    if forall is None:
        return ScalarVariable(name=name, domain=domain, doc=doc)
    return IndexedVariable(name=name, domain=domain, forall=forall, doc=doc)


def _binary_variable(name=None, forall=None, doc=None):
    return variable(name=name, domain=Domain.Binary, forall=forall, doc=doc)
"""

