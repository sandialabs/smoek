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

