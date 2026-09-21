from smoek.core.expr.nodes import ExprLeaf, _wrap_expression_if_needed
from smoek.core.expr.forall import ForAllObject, IndexSetPair
from .components import ModelingComponent, NamedComponent, index

# Conceptually it might make sense to pass index to set constructor,
# i.e.
# i = index()
# I = set()
# s = set(i).forall(i in I)
#
# WEH: We would want to do this for other indexed components as well, right?
#
# v = variable(i,j).forall(i in I, j in J)
#
#   vs
#
# v = variable.forall(i in I, j in J)


class Set(ModelingComponent):
    def __init__(self, name=None, data=None, size=None, doc=None, forall=None):
        super().__init__(name=name, doc=doc)
        self._data = data
        self._size = size
        self._forall = forall

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return self._size

    def __contains__(self, index):
        ForAllObject._latest.append(IndexSetPair(index, self))
        return True


def set(name=None, *, forall=None, doc=None):
    return Set(name=name, doc=doc, forall=forall)


index_set = set


class RangeSet(Set):

    def __init__(self, name, stop):
        super().__init__(name=name)
        self._N = _wrap_expression_if_needed(stop)
        self._size = _wrap_expression_if_needed(stop)

    @property
    def data(self):
        return list(range(self._N + 1))

    def to_string(self):
        return f"range(stop={str(self._N)})"


def range(name=None, *, stop=None):
    return RangeSet(name=name, stop=stop)


class SequenceSet(Set):

    def __init__(self, name, start, stop):
        super().__init__(name=name)
        start = _wrap_expression_if_needed(start)
        stop = _wrap_expression_if_needed(stop)
        self._start = start
        self._stop = stop
        self._size = stop - start + 1

    @property
    def data(self):
        return list(range(self._start, self._stop + 1))

    def to_string(self):
        return f"sequence(start={str(self._start)}, stop={str(self._stop)})"


def sequence(name=None, *, start=None, stop=None):
    return SequenceSet(name, start, stop)
