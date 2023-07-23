import smoek.core.utils


# todo: error checking
class ExprNode(object):
    def __add__(self, right):
        right = _wrap_expression_if_needed(right)
        
        # don't do the addition if right is zero
        if isinstance(right, NumberWrapper) and right._value == 0:
            return self

        return BinaryExprNode(self, right, '+')

    def __radd__(self, left):
        left = _wrap_expression_if_needed(left)

        # don't do the addition if right is zero
        if isinstance(left, NumberWrapper) and left._value == 0:
            return self

        return BinaryExprNode(left, self, '+')

    def __mul__(self, right):
        right = _wrap_expression_if_needed(right)
        
        # don't do the multiplication if right is zero
        if isinstance(right, NumberWrapper):
            if right._value == 0:
                return right
            elif right._value == 1:
                return self
            
        return BinaryExprNode(self, right, '*')

    def __rmul__(self, left):
        left = _wrap_expression_if_needed(left)

        # don't do the addition if right is zero
        if isinstance(left, NumberWrapper):
            if left._value == 0:
                return left
            elif left._value == 1:
                return self
        
        return BinaryExprNode(left, self, '*')

    def __le__(self, right):
        return BinaryExprNode(self, _wrap_expression_if_needed(right), '<=')

    def __ge__(self, right):
        return BinaryExprNode(self, _wrap_expression_if_needed(right), '>=')

    def __eq__(self, right):
        return BinaryExprNode(self, _wrap_expression_if_needed(right), '==')

    def to_list(self):
        return smoek.core.utils.to_list(self)

class ExprLeaf(ExprNode):
    def __init__(self):
        pass

    def to_string(self):
        raise NotImplementedError('Derived classes must implement this')

class BinaryExprNode(ExprNode):
    def __init__(self, left, right, operation):
        assert isinstance(left, ExprNode)
        assert isinstance(right, ExprNode)
        self._left = left
        self._right = right
        self._operation = operation

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def operation(self):
        return self._operation


class NumberWrapper(ExprLeaf):
    def __init__(self, value):
        self._value = value

    def to_string(self):
        return '{}'.format(self._value)

def _wrap_expression_if_needed(expr):
    if not isinstance(expr, ExprNode):
        if isinstance(expr, float) or isinstance(expr, float) or isinstance(expr, int):
            return NumberWrapper(expr)
        else:
            raise TypeError(f"unsupported operand type(s) in expression {expr} of type {type(expr)}")

    return expr

