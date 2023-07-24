from .expression import ExprLeaf, ExprNode
from .utils import ExpressionPrinter

# todo: error checking
# todo: augment printing 

# TODO: change these classes so that all components are the same
# and the presence of forall indicates that they are indexed

class IndexSetPair(object):
    def __init__(self, index, index_set):
        self._index = index
        self._set = index_set

    @property
    def index(self):
        return self._index

    @property
    def set(self):
        return self._set

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

    def sets_list(self):
        return list(isp.set for isp in self._index_set_pairs)
        
    def to_string(self):
        ret = 'forall ' + ', '.join([f'{isp._index.to_string()} in {isp._index_set.to_string()}' for isp in self._index_set_pairs])
        return ret

def forall(index, In=None):
    return ForAllObject().forall(index, In=In)


class NamedComponent(object):
    def __init__(self, name=None, doc=None):
        self._name = name
        self._doc = doc

    @property
    def name(self):
        assert self._name is not None, "No name specified for this component"
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, doc):
        self._doc = doc

    def __str__(self):
        if self._name is None:
            return 'Unnamed Component'
        return self._name

class ComponentIndicesNode(ExprLeaf):
    def __init__(self, component, indices):
        self._component = component
        if type(indices) is tuple:
            self._indices = indices
        else:
            self._indices = (indices,)

    @property
    def component(self):
        return self._component
    
    @property
    def indices(self):
        return self._indices

class ModelingComponent(NamedComponent):
    def __init__(self, name=None, doc=None):
        super().__init__(name, doc)
        self._forall = None

    def is_scalar(self):
        return self._forall is None
        
    def forall(self, index, In):
        if self._forall is None:
            self._forall = ForAllObject()
        self._forall.forall(index, In=In)
        return self

    def __getitem__(self, indices):
        # TODO: proper error message
        assert self._forall is not None
        return ComponentIndicesNode(self, indices)

    def to_string(self):
        if self._forall is None:
            return f'{self._name}'
        else:
            return f'{self._name}, {self._forall.to_string()}'
