from smoek.core.expression import ExprNode
from smoek.core.set_components import ForAllObject

class SumExprNode(ExprNode):
    def __init__(self, expr, forall):
        assert isinstance(expr, ExprNode)
        assert isinstance(forall, ForAllObject)
        self._expr = expr
        self._forall = forall

def smoek_sum(expr, forall):
    return SumExprNode(expr=expr, forall=forall)
    
