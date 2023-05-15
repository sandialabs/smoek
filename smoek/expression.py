def _wrap_expression_if_needed(expr):
    if not isinstance(expr, ExprNode):
        isinstance(expr, float) or isinstance(expr, int)
        return Number(expr)
    return expr

def addition_expr_node(left, right):
    return BinaryExprNode(left, _wrap_expression_if_needed(right), '+')

def multiplication_expr_node(left, right):
    return BinaryExprNode(left, _wrap_expression_if_needed(right), '*')

class ExprNode(object):
    pass

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
    
    def __add__(self, right):
        return addition_expr_node(self, right)

    def __mul__(self, right):
        return multiplication_expr_node(self, right)

class ExprLeaf(ExprNode):
    def __init__(self):
        pass

    def tostring(self):
        raise NotImplementedError('Derived classes must implement this')

    def __add__(self, right):
        return addition_expr_node(self, right)

    def __mul__(self, right):
        return multiplication_expr_node(self, right)

class Variable(ExprLeaf):
    def __init__(self, name):
        self._name = name
        self._indexed = False

    def tostring(self):
        return self._name

class Number(ExprLeaf):
    def __init__(self, value):
        self._value = value

    def tostring(self):
        return '{}'.format(self._value)

class Parameter(ExprLeaf):
    def __init__(self, name):
        self._name = name

    def tostring(self):
        return self._name

class ExpressionPrinter:
    def __init__(self):
        self._depth = 0

    def print_expression(self, expr):
        assert self._depth == 0
        self._depth_first_walk(expr)
        assert self._depth == 0
        
    def _depth_first_walk(self, expr):
        if isinstance(expr, ExprLeaf):
            self._visit(expr)
        else:
            self._visit(expr)
            self._depth += 1
            self._depth_first_walk(expr.left())
            self._depth_first_walk(expr.right())
            self._depth -= 1
            
    def _visit(self, expr):
        if isinstance(expr, BinaryExprNode):
            print('{}{}'.format(' '*self._depth*3, expr.operation()))
        else:
            print('{}{}'.format(' '*self._depth*3, expr.tostring()))

if __name__ == '__main__':
    x = Variable('x')
    y = Parameter('y')
    expr = x*y+x+y*42
    ExpressionPrinter().print_expression(expr)
