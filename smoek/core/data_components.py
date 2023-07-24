from .components import ModelingComponent
from .expression import ExprLeaf

class Parameter(ModelingComponent, ExprLeaf):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)

def parameter(name=None, doc=None):
    return Parameter(name=name, doc=doc)
