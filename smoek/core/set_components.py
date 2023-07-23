from .components import NamedComponent, ScalarComponent, IndexedComponent

##
## INDEX
##

class Index(NamedComponent):
    def __init__(self, name=None):
        super().__init__(name=name)

def index(name=None):
    return Index(name)

##
## SET
##

# TODO : should this be "ScalarSet"?
class ScalarSet(ScalarComponent):
    def __init__(self, name=None, doc=None):
        super().__init__(name=name, doc=doc)

class IndexedSet(IndexedComponent):
    def __init__(self, name=None, forall=None, doc=None):
        super().__init__(name=name, forall=forall, doc=doc)

def set(name=None, forall=None, doc=None):
    if forall is None:
        return ScalarSet(name=name)
    return IndexedSet(name=name, forall=forall)


class IndexSetPair(object):
    def __init__(self, index, index_set):
        self._index = index
        self._index_set = index_set

    @property
    def index(self):
        return self._index

    @property
    def index_set(self):
        return self._index_set

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

    def indices_list(self):
        return list(isp.index for isp in self._index_set_pairs)
        
    def to_string(self):
        ret = 'forall ' + ', '.join([f'{isp._index.to_string()} in {isp._index_set.to_string()}' for isp in self._index_set_pairs])
        return ret

def forall(index, In=None):
    return ForAllObject().forall(index, In=In)
