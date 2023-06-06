from .expression import ExprLeaf, VariableIndexExpression
from .utils import ExpressionPrinter, to_list

# todo: error checking
# todo: augment printing 

class Index(object):
    def __init__(self, name):
        self._name = name

    def to_string(self):
        return self._name

class Set(object):
    def __init__(self, name):
        self._name = name

    def to_string(self):
        return self._name

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

    def to_list(self):
        return to_list(self)

class IndexedVariable(IndexableComponent):
    def __init__(self, name=None):
        super().__init__(name)
        self._value = None
                
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
        raise RuntimeError("Cannot get the value of an indexed variable without specifying the index")

    @value.setter
    def value(self, v):
        self._value = v
        for var in self._used_indices.values():
            var._value = v

class SingleVariable(ExprLeaf):
    def __init__(self, name=None):
        super().__init__()
        self._name = name
        self._value = None

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

def variable(index=None, *, name=None, value=None):
    if index is None:
        v = SingleVariable(name=name)
        if value is not None:
            v.value = value
        return v
    else:
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
    i = Index('i')
    j = Index('j')
    A = Set('A')
    x = Variable('x')
    f = forall(i, In=A).forall(j, In=A)
    y = Variable('y').forall(i, In=A).forall(j, In=A)
    print(y.to_string())

    c = Constraint('c', expr=x <= y[i,j]).forall(i, In=A).forall(j, In=A)
    print(c.to_string())
    
    expr = x+x*y[i,j]
    ExpressionPrinter().print_expression(expr)
