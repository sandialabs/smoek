from .components import NamedComponent, ScalarComponent, IndexedComponent
from .expression import SetIndexExpression

##
## INDEX
##

class Index(NamedComponent):
    def __init__(self, name=None):
        super().__init__(name)

def index(name=None):
    return Index(name)


##
## SET
##

# TODO : should this be "ScalarSet"?
class ScalarSet(ScalarComponent):
    def __init__(self, name=None):
        super().__init__(name)

class IndexedSet(IndexedComponent):
    def __init__(self, name=None, forall=None):
        super().__init__(name=name, forall=forall)

# TODO: This name is clumsy, but "set" is a reserved word?
def index_set(name=None, forall=None):
    if forall is None:
        return ScalarSet(name=name)
    return IndexedSet(name=name, forall=forall)


class IndexSetPair(object):
    def __init__(self, index, index_set):
        self._index = index
        self._index_set = index_set

class ForAllObject(object):
    def __init__(self):
        self._index_set_pairs = list()
        self._filter_expressions = list()

    def forall(self, index, In=None):
        self._index_set_pairs.append(IndexSetPair(index, In))
        return self
    
    def suchthat(self, expr):
        self._filter_expressions.append(expr)
        return self
    
    def to_string(self):
        ret = 'forall ' + ', '.join([f'{isp._index.to_string()} in {isp._index_set.to_string()}' for isp in self._index_set_pairs])
        return ret

def forall(index, In=None):
    return ForAllObject().forall(index, In=In)
