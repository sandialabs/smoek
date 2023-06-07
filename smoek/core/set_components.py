import math

from .expression import SetIndexExpression

##
## INDEX
##

class Index(object):
    def __init__(self, name=None):
        self._name = name

    def to_string(self):
        return self._name

def index(name=None):
    return Index(name)

##
## SET
##

class Set(object):
    def __init__(self, name=None):
        self._name = name
        self._elements = []

    @property
    def name(self):
        assert self._name is not None, "No name specified for this set"
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, v):
        self._elements = v

    def to_string(self):
        return self._name

#
# WEH: How specify a 1-d, or n-d array?
#
class IndexedSet(object):
    def __init__(self, name=None):
        self._name = name
        self._used_indices = {}
        self._elements = []

    def to_string(self):
        return self._name

    @property
    def name(self):
        assert self._name is not None, "No name specified for this set"
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    def __getitem__(self, indices):
        tmp = self._used_indices.get(indices, None)
        if tmp is not None:
            return tmp
        tmp = SetIndexExpression(self, indices)
        self._used_indices[indices] = tmp
        return tmp

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, v):
        self._elements = v
        for _set in self._used_indices.values():
            _set._elements = v

def index_set(*args):
    if len(args) == 0:
        # index_set()
        return Set()

    elif len(args) == 1:
        if args[0] == 1:
            # index_set(1)
            return Set()
        elif type(args[0]) == str:
            # index_set('x')
            return Set(name=args[0])
        else:
            # index_set(2) or index_set([2,3])
            # TODO: Configure the index dimensions "args[0]"
            return IndexedSet()
    else:
        # index_set('x', 2) or index_set('x', [2,3])
        assert len(args) == 2, "The index_set() function only takes two arguments"
        # TODO: Configure the index dimensions "args[1]"
        return IndexedSet(name=args[0])

