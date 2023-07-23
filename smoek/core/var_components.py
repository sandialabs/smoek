from enum import Enum

from .components import ScalarComponent, IndexedComponent
from .expression import ExprLeaf

class Domain(Enum):
    Reals = 1
    Binary = 2
                
class ScalarVariable(ScalarComponent, ExprLeaf):
    def __init__(self, name=None, domain=None):
        super().__init__(name)
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
    def __init__(self, name=None, domain=None, forall=None):
        super().__init__(name, forall)
        self._domain = domain

    @property
    def domain(self):
        return self._domain

def variable(name=None, domain=None, forall=None):
    if forall is None:
        return ScalarVariable(name, domain=domain)
    return IndexedVariable(name=name, domain=domain, forall=forall)


def binary_variable(name=None, forall=None):
    return variable(name=name, domain=Domain.Binary, forall=forall)

# def variable(index=None, *, name=None, value=None):
#     if index is None:
#         v = SingleVariable(name=name)
#         if value is not None:
#             v.value = value
#         return v
#     else:
#         # TODO: Configure the index dimensions "args[0]"
#         v = IndexedVariable(name=name)
#         if value is not None:
#             v.value = value
#         return v

