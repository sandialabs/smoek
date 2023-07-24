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
