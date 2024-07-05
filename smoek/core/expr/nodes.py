# TODO: error checking

from enum import StrEnum


class ExpressionType(StrEnum):
    add = "+"
    sub = "-"
    neg = "neg"
    mul = "*"
    div = "/"
    pow = "pow"
    sum = "sum"
    prod = "prod"
    log = "log"
    exp = "expr"
    sin = "sin"
    cos = "cos"
    tan = "tan"
    asin = "asin"
    acos = "acos"
    atan = "atan"
    variable = "variable"
    parameter = "parameter"
    constant = "constant"
    leq = "<="
    eq = "=="
    geq = ">="
    indexed_component = "indexed_component"  # WEH: This is really a reference to an element in a indexed component, right?


class ExprNode(object):
    def __add__(self, right):
        right = _wrap_expression_if_needed(right)

        # don't do the addition if right is zero
        if isinstance(right, NumberWrapper) and right._value == 0:
            return self

        return BinaryExprNode(self, right, ExpressionType.add)

    def __radd__(self, left):
        left = _wrap_expression_if_needed(left)

        # don't do the addition if right is zero
        if isinstance(left, NumberWrapper) and left._value == 0:
            return self

        return BinaryExprNode(left, self, ExpressionType.add)

    def __mul__(self, right):
        right = _wrap_expression_if_needed(right)

        # don't do the multiplication if right is zero
        if isinstance(right, NumberWrapper):
            if right._value == 0:
                return right
            elif right._value == 1:
                return self

        return BinaryExprNode(self, right, ExpressionType.mul)

    def __rmul__(self, left):
        left = _wrap_expression_if_needed(left)

        # don't do the addition if right is zero
        if isinstance(left, NumberWrapper):
            if left._value == 0:
                return left
            elif left._value == 1:
                return self

        return BinaryExprNode(left, self, ExpressionType.mul)

    def __sub__(self, right):
        right = _wrap_expression_if_needed(right)

        # don't do the addition if right is zero
        if isinstance(right, NumberWrapper) and right._value == 0:
            return self

        return BinaryExprNode(self, right, ExpressionType.sub)

    def __rsub__(self, left):
        left = _wrap_expression_if_needed(left)

        # don't do the addition if right is zero
        if isinstance(left, NumberWrapper) and left._value == 0:
            return self

        return BinaryExprNode(left, self, ExpressionType.sub)

    def __neg__(self):
        return UnaryExprNode(self, ExpressionType.neg)

    def __truediv__(self, right):
        right = _wrap_expression_if_needed(right)

        # don't do the multiplication if right is zero
        if isinstance(right, NumberWrapper):
            if right._value == 0:
                raise ZeroDivisionError("division by zero")
            elif right._value == 1:
                return self

        return BinaryExprNode(self, right, ExpressionType.div)

    def __rtruediv__(self, left):
        left = _wrap_expression_if_needed(left)

        # don't do the addition if left is zero
        if isinstance(left, NumberWrapper) and left._value == 0:
            return NumberWrapper(0)

        return BinaryExprNode(left, self, ExpressionType.div)

    def __le__(self, right):
        return BinaryExprNode(
            self, _wrap_expression_if_needed(right), ExpressionType.leq
        )

    def __ge__(self, right):
        return BinaryExprNode(
            self, _wrap_expression_if_needed(right), ExpressionType.geq
        )

    def __eq__(self, right):
        return BinaryExprNode(
            self, _wrap_expression_if_needed(right), ExpressionType.eq
        )

    def __pow__(self, right):
        right = _wrap_expression_if_needed(right)

        # don't do the multiplication if right is zero
        if isinstance(right, NumberWrapper):
            if right._value == 0:
                return NumberWrapper(1)
            elif right._value == 1:
                return self

        return BinaryExprNode(
            self, _wrap_expression_if_needed(right), ExpressionType.pow
        )

    def is_leaf(self):
        return False

    def args(self):
        raise NotImplementedError("Should be implemented by derived classes")

    def etype(self):
        raise NotImplementedError("Should be implemented by derived classes")

    def __str__(self) -> str:
        from smoek.core.utils import expr_to_string

        return expr_to_string(self)

    def __repr__(self) -> str:
        from smoek.core.utils import expr_to_string

        return expr_to_string(self)


class ExprLeaf(ExprNode):
    def __init__(self):
        pass

    def to_string(self):
        raise NotImplementedError("Derived classes must implement this")

    def is_leaf(self):
        return True

    def args(self):
        return tuple()


class BinaryExprNode(ExprNode):
    def __init__(self, left, right, operation):
        assert isinstance(left, ExprNode)
        assert isinstance(right, ExprNode)
        self._left = left
        self._right = right
        self._operation = operation

    def etype(self):
        return self._operation

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def operation(self):
        return self._operation

    def args(self):
        return (self.left, self.right)


class UnaryExprNode(ExprNode):
    def __init__(self, expr, operation):
        expr = _wrap_expression_if_needed(expr)
        assert isinstance(
            expr, ExprNode
        ), f"expression is not an instance of ExprNode: {type(expr)}"
        self._arg = expr
        self._operation = operation

    def etype(self):
        return self._operation

    @property
    def arg(self):
        return self._arg

    @property
    def operation(self):
        return self._operation

    def args(self):
        return (self.arg,)


class NumberWrapper(ExprLeaf):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def to_string(self):
        return "{}".format(self._value)

    def etype(self):
        return ExpressionType.constant


def _wrap_expression_if_needed(expr):
    if not isinstance(expr, ExprNode):
        if isinstance(expr, float) or isinstance(expr, int):
            return NumberWrapper(expr)
        else:
            raise TypeError(
                f"unsupported operand type(s) in expression {expr} of type {type(expr)}"
            )

    return expr


#
# WEH - This class name is not obvious.  Maybe something like IndexedComponentRefNode?
#
class ComponentIndicesNode(ExprLeaf):
    def __init__(self, component, indices):
        self._component = component
        if type(indices) is tuple:
            self._indices = indices
        else:
            self._indices = (indices,)

    def etype(self):
        return ExpressionType.indexed_component

    @property
    def component(self):
        return self._component

    @property
    def indices(self):
        return self._indices

    def to_string(self):
        indices = [
            index.to_string() if hasattr(index, "to_string") else str(index)
            for index in self._indices
        ]
        return f'{self._component.name()}[{", ".join(indices)}]'
