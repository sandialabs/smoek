from .components import IndexedComponent


class Parameter(IndexedComponent):
    def __init__(self, name=None):
        super().__init__(name)

    def value(self, v):
        self._value = v

def parameter(index=None, name=None, value=None):
    p = Parameter(name=name)
    if value is not None:
        p.value(value)
    return p

