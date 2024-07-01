from .components import ModelingComponent
from .expr_components import ExprNode
from .utils import expr_to_string


class Constraint(ModelingComponent):
    def __init__(self, expr=None, name=None, doc=None):
        super().__init__(name=name, doc=doc)
        if expr is not None:
            assert isinstance(expr, ExprNode)
        self._expr = expr

    def index_set(self):
        if self._forall is None:
            return None
        return self._forall.indices_list()

    def forall(self, index, In):
        # TODO: assert index are present in ComponentIndicesNode in self._expr
        return super().forall(index, In)

    def to_string(self):
        return f"{super().to_string()} : {expr_to_string(self._expr)}"


def constraint(expr=None, name=None, doc=None):
    return Constraint(expr=expr, name=name, doc=doc)
