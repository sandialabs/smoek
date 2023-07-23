from .expression import ExprLeaf, ExprNode
from .utils import ExpressionPrinter

# todo: error checking
# todo: augment printing 

# TODO: change these classes so that all components are the same
# and the presence of forall indicates that they are indexed

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

    
class ScalarComponent(NamedComponent):
    pass


class IndexedComponent(NamedComponent):
    def __init__(self, name=None, doc=None, forall=None):
        super().__init__(name, doc)
        self._forall = forall
        
    def forall(self, index, In):
        from core.set_components import ForAllObject
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

class ScalarExpression(ScalarComponent):
    def __init__(self, name, expr, doc=None):
        super().__init__(name=name, doc=doc)
        assert expr is not None
        assert isinstance(expr, ExprNode)
        self._expr = expr

    @property
    def expr(self):
        return self._expr
        
class IndexedExpression(IndexedComponent):
    def __init__(self, name, expr, forall, doc=None):
        super().__init__(name=name, forall=forall, doc=doc)
        assert expr is not None
        assert isinstance(expr, ExprNode)
        self._expr = expr

    @property
    def expr(self):
        self._expr = expr

    # don't allow for now - likely later
    # def expr(self, expr):
    #     self._expr = expr

    def to_string(self):
        ret = super().to_string()
        ret += ExpressionPrinter().expression_to_string(self._expr)
        return ret

class ScalarConstraint(ScalarExpression):
    def __init__(self, name, expr, doc=None):
        super().__init__(name, expr, doc=doc)

class IndexedConstraint(IndexedExpression):
    def __init__(self, name, expr, forall, doc=None):
        super().__init__(name=name, expr=expr, forall=forall, doc=doc)

class ScalarObjective(ScalarExpression):
    def __init__(self, name, expr, doc=None):
        super().__init__(name=name, expr=expr, doc=doc)

class IndexedObjective(IndexedExpression):
    def __init__(self, name, expr, forall, doc=None):
        super().__init__(name=name, expr=expr, forall=forall, doc=doc)

def constraint(name=None, expr=None, forall=None, doc=None):
    assert expr is not None
    if forall is None:
        return ScalarConstraint(name=name, expr=expr, doc=doc)
    return IndexedConstraint(name=name, expr=expr, forall=forall, doc=doc)

def objective(name=None, expr=None, forall=None, doc=None):
    assert expr is not None
    if forall is None:
        return ScalarObjective(name=name, expr=expr, doc=doc)
    return IndexedObjective(name=name, expr=expr, forall=forall, doc=doc)

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
