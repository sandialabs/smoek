from .expression import ExprLeaf
from .utils import ExpressionPrinter

# todo: error checking
# todo: augment printing 
   
class NamedComponent(object):
    def __init__(self, name=None):
        self._name = name

    @property
    def name(self):
        assert self._name is not None, "No name specified for this component"
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __str__(self):
        if self._name is None:
            return 'Unnamed Component'
        return self._name

    
class ScalarComponent(NamedComponent):
    pass


# TODO: not good that a constraint can also be an expression leaf
class IndexedComponent(NamedComponent):
    def __init__(self, name=None, forall=None):
        super().__init__(name)
        self._forall = forall
        
    def forall(self, index, In):
        if self._forall is None:
            self._forall = ForAllObject()
        self._forall.forall(index, In=In)
        return self

    def __getitem__(self, indices):
        # TODO: We may want to cache these
        return ComponentIndicesNode(self, indices)

    def to_string(self):
        if self._forall is None:
            return f'{self._name}'
        else:
            return f'{self._name}, {self._forall.to_string()}'

class ComponentIndicesNode(ExprLeaf):
    def __init__(self, component, indices):
        self._component = component
        self._indices = indices

    @property
    def component(self):
        return self._component
    
    @property
    def indices(self):
        return self._indices

# TODO: Move this
class Constraint(IndexedComponent):
    def __init__(self, name=None):
        super().__init__(name)
        self._expr = expr

    def expr(self, _expr):
        self._expr = _expr

    def to_string(self):
        ret = super().to_string()
        ret += ExpressionPrinter().expression_to_string(self._expr)
        return ret


# if __name__ == '__main__':
#     i = index('i')
#     j = index('j')
#     A = index_set('A')
#     x = variable('x')
#     f = forall(i, In=A).forall(j, In=A)
#     y = variable('y').forall(i, In=A).forall(j, In=A)
#     print(y.to_string())

#     c = Constraint('c', expr=x <= y[i,j]).forall(i, In=A).forall(j, In=A)
#     print(c.to_string())
    
#     expr = x+x*y[i,j]
#     ExpressionPrinter().print_expression(expr)
