import math

from .components import ScalarComponent, IndexedComponent
from .expression import ExprLeaf

# Todo: think about having a single object that has a forall
# or doesn't have a forall to differentiate scalar vs indexed?
class IndexedVariable(IndexedComponent):
    def __init__(self, name=None, forall=None):
        super().__init__(name, forall)
                
class ScalarVariable(ScalarComponent, ExprLeaf):
    def __init__(self, name=None):
        super().__init__(name)

    def to_string(self):
        return self.name

def variable(name=None, forall=None):
    if forall is None:
        return ScalarVariable(name)
    return IndexedVariable(name=name, forall=forall)

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

