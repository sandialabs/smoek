from smoek.core.expression import ExprNode
from smoek.core.components import ForAllObject

class SumExprNode(ExprNode):
    def __init__(self, expr):
        assert isinstance(expr, ExprNode)
        self._expr = expr
        self._forall = None

    def forall(self, index, In=None):
        if self._forall is None:
            self._forall = ForAllObject()
        self._forall.forall(index, In=In)
        return self

def smoek_sum(expr):
    return SumExprNode(expr=expr)
    
