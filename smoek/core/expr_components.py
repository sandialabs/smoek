from .components import ModelingComponent

class Expression(ModelingComponent):
    def __init__(self, name=None, expr=None, doc=None):
        super().__init__(name=name, doc=doc)
        assert expr is not None
        self._expr = expr

    @property
    def expr(self):
        return self._expr

class Constraint(Expression):
    def __init__(self, name=None, expr=None, doc=None):
        super().__init__(name=name, expr=expr, doc=doc)

def constraint(name=None, expr=None, doc=None):
    return Constraint(name=name, expr=expr, doc=doc)

class Objective(Expression):
    def __init__(self, name=None, expr=None, doc=None):
        super().__init__(name=name, expr=expr, doc=doc)

def objective(name=None, expr=None, doc=None):
    return Objective(name=name, expr=expr, doc=doc)
    
