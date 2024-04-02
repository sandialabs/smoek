from .components import ModelingComponent, NamedComponent, ComponentIndicesNode

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

class ScalarSet(Set):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)

class IndexedSet(Set):
    def __init__(self, name=None, forall=None, doc=None):
        super().__init__(name=name, doc=doc)
        self._forall = forall

    def __getitem__(self, indices):
        return ComponentIndicesNode(self, indices)

def index_set(name=None, forall=None, doc=None):
    if forall is None:
        return ScalarSet(name=name, doc=doc)
    else:
        return IndexedSet(name=name, forall=forall, doc=doc)
