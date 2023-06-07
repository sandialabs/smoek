import math

from .expression import ExprLeaf, VariableIndexExpression, SetIndexExpression
from .utils import ExpressionPrinter

# todo: error checking
# todo: augment printing 

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

##
##
##

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

# TODO: not good that a constraint can also be an expression leaf
class IndexableComponent(ExprLeaf):
    def __init__(self, name=None):
        self._name = name
        self._forall = None
        self._used_indices = {}

    def forall(self, index, In):
        if self._forall is None:
            self._forall = ForAllObject()
        self._forall.forall(index, In=In)
        return self

    def to_string(self):
        if self._forall is None:
            return f'{self._name}'
        else:
            return f'{self._name}, {self._forall.to_string()}'

class IndexedVariable(IndexableComponent):
    def __init__(self, name=None):
        super().__init__(name)
        self._value = math.nan
                
    @property
    def name(self):
        assert self._name is not None, "No name specified for this variable"
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    def __getitem__(self, indices):
        tmp = self._used_indices.get(indices, None)
        if tmp is not None:
            return tmp
        tmp = VariableIndexExpression(self, indices)
        self._used_indices[indices] = tmp
        return tmp

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        for var in self._used_indices.values():
            var._value = v

class SingleVariable(ExprLeaf):
    def __init__(self, name=None):
        super().__init__()
        self._name = name
        self._value = math.nan

    @property
    def name(self):
        assert self._name is not None, "No name specified for this variable"
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    def to_string(self):
        return self.name

def variable(index=None, *, name=None, value=None):
    if index is None:
        v = SingleVariable(name=name)
        if value is not None:
            v.value = value
        return v
    else:
        # TODO: Configure the index dimensions "args[0]"
        v = IndexedVariable(name=name)
        if value is not None:
            v.value = value
        return v

class Parameter(IndexableComponent):
    def __init__(self, name=None):
        super().__init__(name)

    def value(self, v):
        self._value = v

def parameter(index=None, name=None, value=None):
    p = Parameter(name=name)
    if value is not None:
        p.value(value)
    return p

class Constraint(IndexableComponent):
    def __init__(self, name=None):
        super().__init__(name)
        self._expr = expr

    def expr(self, _expr):
        self._expr = _expr

    def to_string(self):
        ret = super().to_string()
        ret += ExpressionPrinter().expression_to_string(self._expr)
        return ret

def forall(index, In=None):
    return ForAllObject().forall(index, In=In)

if __name__ == '__main__':
    i = index('i')
    j = index('j')
    A = index_set('A')
    x = variable('x')
    f = forall(i, In=A).forall(j, In=A)
    y = variable('y').forall(i, In=A).forall(j, In=A)
    print(y.to_string())

    c = Constraint('c', expr=x <= y[i,j]).forall(i, In=A).forall(j, In=A)
    print(c.to_string())
    
    expr = x+x*y[i,j]
    ExpressionPrinter().print_expression(expr)
