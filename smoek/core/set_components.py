from .components import ModelingComponent, NamedComponent
from .expr_components import ExprLeaf


# should we include attribute for dimension of index?
# can indices be ExprLeafs (e.g. for construction of filter expressions based on value)?
# would imply all indices are numeric - may be a sensible restriction
class Index(NamedComponent, ExprLeaf):
    def __init__(self, name=None):
        super().__init__(name=name)

    def to_string(self):
        return str(self)


# class NumericIndex(Index, ExprLeaf):
#     def __init__(self, name=None):
#         super().__init__(name=name)


def index(name=None):
    return Index(name)


# Conceptually it might make sense to pass index to set constructor,
# i.e.
# i = index()
# I = set()
# s = set(i).forall(i, in = I)


class Set(ModelingComponent):
    def __init__(self, name=None, data=None, size=None, doc=None):
        super().__init__(name=name, doc=doc)
        self._data = data
        self._size = size

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return self._size


def set(name=None, doc=None):
    return Set(name=name, doc=doc)


# I don't think we need to differentiate between ScalarSet and IndexedSet
# Calling set().forall(...) will automatically create an indexed set
class ScalarSet(Set):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)


class IndexedSet(Set):
    def __init__(self, name=None, forall=None, doc=None):
        super().__init__(name=name, doc=doc)
        self._forall = forall

    # Is already implemented in ModelingComponent
    # def __getitem__(self, indices):
    #     return ComponentIndicesNode(self, indices)


def index_set(name=None, forall=None, doc=None):
    if forall is None:
        return ScalarSet(name=name, doc=doc)
    else:
        return IndexedSet(name=name, forall=forall, doc=doc)
