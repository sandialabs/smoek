from expression import ExprLeaf, VariableIndexExpression
from utils import ExpressionPrinter

# todo: error checking
# todo: augment printing 
class Index(object):
    def __init__(self, name):
        self._name = name

    def tostring(self):
        return self._name

class Set(object):
    def __init__(self, name):
        self._name = name

    def tostring(self):
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
    
    def tostring(self):
        ret = 'forall ' + ', '.join([f'{isp._index.tostring()} in {isp._index_set.tostring()}' for isp in self._index_set_pairs])
        return ret

# TODO: not good that a constraint can also be an expression leaf
class IndexableComponent(ExprLeaf):
    def __init__(self, name):
        self._name = name
        self._forall = None

    def forall(self, index, In):
        if self._forall is None:
            self._forall = ForAllObject()
        self._forall.forall(index, In=In)
        return self

    def tostring(self):
        if self._forall is None:
            return f'{self._name}'
        else:
            return f'{self._name}, {self._forall.tostring()}'

class Variable(IndexableComponent):
    def __init__(self, name):
        super().__init__(name)
                
    def __getitem__(self, indices):
        return VariableIndexExpression(self, indices)

class Parameter(IndexableComponent):
    def __init__(self, name):
        super().__init__(name)

class Constraint(IndexableComponent):
    def __init__(self, name, expr):
        super().__init__(name)
        self._expr = expr

    def tostring(self):
        ret = super().tostring()
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
    print(y.tostring())

    c = Constraint('c', expr=x <= y[i,j]).forall(i, In=A).forall(j, In=A)
    print(c.tostring())
    
    expr = x+x*y[i,j]
    ExpressionPrinter().print_expression(expr)
