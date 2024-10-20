from smoek.core.expr.nodes import ExprNode
from .components import ModelingComponent, index


class Constraint(ModelingComponent):
    def __init__(self, name=None, expr=None, doc=None):
        super().__init__(name=name, doc=doc)
        self._expr = expr

    def expr(self, expr=None):
        if expr is None:
            return self._expr
        self._expr = expr
        return self

    def forall(self, iset_pair):
        # TODO: assert index are present in ComponentIndicesNode in self._expr
        return super().forall(iset_pair)

    def to_string(self):
        from smoek.core.utils import expr_to_string

        return f"{super().to_string()} : {expr_to_string(self._expr)}"


def constraint(name=None):
    return Constraint(name=name)
