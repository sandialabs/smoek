from .components import ScalarComponent, IndexedComponent
from .expression import ExprLeaf

class ScalarParameter(ScalarComponent, ExprLeaf):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)

class IndexedParameter(IndexedComponent):
    def __init__(self, name=None, forall=None, doc=None):
        super().__init__(name=name, forall=forall, doc=doc)
    
def parameter(name=None, forall=None, doc=None):
    if forall is None:
        return ScalarParameter(name=name, doc=doc)
    return IndexedParameter(name=name, forall=forall, doc=doc)

