from .components import ModelingComponent
from .expr_components import ExprNode

class Expression(ModelingComponent, ExprNode):
    def __init__(self, name=None, expr=None, doc=None):
        super().__init__(name=name, doc=doc)
        assert expr is not None
        self._expr = expr

    @property
    def expr(self):
        return self._expr
    
    # TODO: Indexed Expressions are not well-defined yet
    # TODO: Move all writer functions into separate class
    def to_string(self):
        return self.name + ' : ' + self._expr.to_string()
    

def expression(name=None, expr=None, doc=None):
    # TODO: Allow <=, ==, etc in expression?
    return Expression(name=name, expr=expr, doc=doc)

# class Constraint(Expression):
#     def __init__(self, name=None, expr=None, doc=None):
#         super().__init__(name=name, expr=expr, doc=doc)

# def constraint(name=None, expr=None, doc=None):
#     return Constraint(name=name, expr=expr, doc=doc)

class Objective(Expression):
    def __init__(self, name=None, expr=None, doc=None, sense=None):
        super().__init__(name=name, expr=expr, doc=doc)

def objective(name=None, expr=None, doc=None, sense=None):
    return Objective(name=name, expr=expr, doc=doc, sense=sense)