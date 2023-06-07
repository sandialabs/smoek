from .expression import ExprLeaf
from .utils import ExpressionPrinter

# todo: error checking
# todo: augment printing 

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
