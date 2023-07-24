from .components import ModelingComponent, NamedComponent

class Index(NamedComponent):
    def __init__(self, name=None):
        super().__init__(name=name)

def index(name=None):
    return Index(name)

class Set(ModelingComponent):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)

def set(name=None, doc=None):
    return Set(name=name, doc=doc)

"""
# TODO : should this be "ScalarSet"?
class ScalarSet(ScalarComponent):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)

class IndexedSet(IndexedComponent):
    def __init__(self, name=None, forall=None, doc=None):
        super().__init__(name=name, forall=forall, doc=doc)

def _set(name=None, forall=None, doc=None):
    if forall is None:
        return ScalarSet(name=name)
    return IndexedSet(name=name, forall=forall)
"""
