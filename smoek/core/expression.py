# todo: error checking
class ExprNode(object):
    def __add__(self, right):
        return addition_expr_node(self, right)

    def __mul__(self, right):
        return multiplication_expr_node(self, right)

    def __le__(self, right):
        return BinaryExprNode(self, _wrap_expression_if_needed(right), 'le')

    def __ge__(self, right):
        return BinaryExprNode(self, _wrap_expression_if_needed(right), 'ge')

    def __eq__(self, right):
        return BinaryExprNode(self, _wrap_expression_if_needed(right), 'eq')

class ExprLeaf(ExprNode):
    def __init__(self):
        pass

    def tostring(self):
        raise NotImplementedError('Derived classes must implement this')

class BinaryExprNode(ExprNode):
    def __init__(self, left, right, operation):
        self._left = left
        self._right = right
        self._operation = operation

    def left(self):
        return self._left

    def right(self):
        return self._right

    def operation(self):
        return self._operation

class NumberWrapper(ExprLeaf):
    def __init__(self, value):
        self._value = value

    def tostring(self):
        return '{}'.format(self._value)

class VariableIndexExpression(ExprLeaf):
    def __init__(self, var, indices):
        self._var = var
        self._indices = indices
        # todo: error checking

    def tostring(self):
        assert self._indices is not None
        indstr = ','.join(ind.tostring() for ind in self._indices)
        return f'{self._var.tostring()}[{indstr}]'

def _wrap_expression_if_needed(expr):
    if not isinstance(expr, ExprNode):
        isinstance(expr, float) or isinstance(expr, int)
        return Number(expr)
    return expr

def addition_expr_node(left, right):
    return BinaryExprNode(left, _wrap_expression_if_needed(right), '+')

def multiplication_expr_node(left, right):
    return BinaryExprNode(left, _wrap_expression_if_needed(right), '*')

