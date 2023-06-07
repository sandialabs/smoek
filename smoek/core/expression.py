import smoek.core.utils


# todo: error checking
class ExprNode(object):
    def __add__(self, right):
        return addition_expr_node(self, _wrap_expression_if_needed(right))

    def __radd__(self, left):
        return addition_expr_node(_wrap_expression_if_needed(left), self)

    def __mul__(self, right):
        return multiplication_expr_node(self, _wrap_expression_if_needed(right))

    def __rmul__(self, left):
        return multiplication_expr_node(_wrap_expression_if_needed(left), self)

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

    def to_string(self):
        return '{}'.format(self._value)

class SetIndexExpression(ExprLeaf):
    def __init__(self, _set, indices):
        self._set = _set
        if type(indices) is not tuple:
            indices = (indices,)
        self._indices = indices
        self._elements = _set._elements      # TODO: copy here

    @property
    def name(self):
        assert self._set.name is not None, "No name specified for this variable"
        indstr = ','.join(ind.to_string() if isinstance(ind, ExprLeaf) else str(ind) for ind in self._indices)
        return f"{self._set.name}[{indstr}]"

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, v):
        self._elements = v

    def to_string(self):
        return self.name

class VariableIndexExpression(ExprLeaf):
    def __init__(self, var, indices):
        self._var = var
        if type(indices) is not tuple:
            indices = (indices,)
        self._indices = indices
        self._value = var._value

    @property
    def name(self):
        assert self._var.name is not None, "No name specified for this variable"
        indstr = ','.join(ind.to_string() if isinstance(ind, ExprLeaf) else str(ind) for ind in self._indices)
        return f"{self._var.name}[{indstr}]"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    def to_string(self):
        return self.name

def _wrap_expression_if_needed(expr):
    if not isinstance(expr, ExprNode):
        isinstance(expr, float) or isinstance(expr, int)
        return NumberWrapper(expr)
    return expr

def addition_expr_node(left, right):
    return BinaryExprNode(left, right, '+')

def multiplication_expr_node(left, right):
    return BinaryExprNode(left, right, '*')

