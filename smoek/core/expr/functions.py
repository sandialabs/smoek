from smoek.core.expr.nodes import ExprNode, UnaryExprNode
from smoek.core.expr.forall import ForAllObject


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


def sum(expr):
    return SumExprNode(expr=expr)


class ProdExprNode(ExprNode):
    def __init__(self, expr):
        assert isinstance(expr, ExprNode)
        self._expr = expr
        self._forall = None

    def forall(self, index, In=None):
        if self._forall is None:
            self._forall = ForAllObject()
        self._forall.forall(index, In=In)
        return self


def prod(expr):
    return ProdExprNode(expr=expr)


def log(expr):
    return UnaryExprNode(expr=expr, operation="log")


def exp(expr):
    return UnaryExprNode(expr=expr, operation="exp")


def sin(expr):
    return UnaryExprNode(expr=expr, operation="sin")


def cos(expr):
    return UnaryExprNode(expr=expr, operation="cos")


def tan(expr):
    return UnaryExprNode(expr=expr, operation="tan")
