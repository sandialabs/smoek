from smoek.core.expr.nodes import ExprNode
from .components import ModelingComponent


class Expression(ModelingComponent, ExprNode):
    def __init__(self, name=None, expr=None, doc=None):
        super().__init__(name=name, doc=doc)
        self._expr = expr

    def expr(self, expr=None):
        if expr is None:
            return self._expr
        self._expr = expr
        return self

    # TODO: Indexed Expressions are not well-defined yet
    # TODO: Move all writer functions into separate class
    def to_string(self):
        return self.name()  # + " : " + self._expr.to_string()


def expression(name=None, expr=None, doc=None):
    # TODO: Allow <=, ==, etc in expression?
    return Expression(name=name, expr=expr, doc=doc)


minimize = True
maximize = False


class Objective(ModelingComponent, ExprNode):
    def __init__(self, name=None, expr=None, doc=None):
        super().__init__(name=name, doc=doc)
        self._sense = True
        self._expr = expr

    def expr(self, expr=None):
        if expr is None:
            return self._expr
        self._expr = expr
        return self

    def sense(self, sense=None):
        if sense is None:
            return self._sense
        self._sense = sense
        return self

    def minimize(self, expr=None):
        if expr is not None:
            self._expr = expr
        self._sense = True
        return self

    def maximize(self, expr=None):
        if expr is not None:
            self._expr = expr
        self._sense = False
        return self

    def to_string(self):
        return self.name()  # + " : " + self._expr.to_string()


def objective(name=None):
    return Objective(name=name)
