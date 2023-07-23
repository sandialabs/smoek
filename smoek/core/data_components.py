from .components import ScalarComponent, IndexedComponent
from .expression import ExprLeaf

class ScalarParameter(ScalarComponent, ExprLeaf):
    def __init__(self, name=None):
        super().__init__(name)

class IndexedParameter(IndexedComponent):
    def __init__(self, name=None, forall=None):
        super().__init__(name, forall)
    
def parameter(name=None, forall=None):
    if forall is None:
        return ScalarParameter(name)
    return IndexedParameter(name=name, forall=forall)

