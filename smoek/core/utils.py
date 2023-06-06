import smoek.core.expression

class ExpressionPrinter:
    def __init__(self):
        self._depth = 0

    def expression_to_string(self, expr):
        assert self._depth == 0
        self._ret = ''
        
        self._depth_first_walk(expr)
        assert self._depth == 0

        self._ret += '\n'
        ret = self._ret
        self._ret = None
        return ret

    def print_expression(self, expr):
        print(self.expression_to_string(expr))
        
    def _depth_first_walk(self, expr):
        if isinstance(expr, smoek.core.expression.ExprLeaf):
            self._visit(expr)
        else:
            self._visit(expr)
            self._depth += 1
            self._depth_first_walk(expr.left())
            self._depth_first_walk(expr.right())
            self._depth -= 1
            
    def _visit(self, expr):
        if isinstance(expr, smoek.core.expression.BinaryExprNode):
            self._ret += '\n{}{}'.format(' '*self._depth*3, expr.operation())
        else:
            self._ret += '\n{}{}'.format(' '*self._depth*3, expr.to_string())


class ExpressionToList:
    def expression_to_list(self, expr):
        return self._depth_first_walk(expr)

    def _depth_first_walk(self, expr):
        if isinstance(expr, smoek.core.expression.ExprLeaf):
            return self._visit(expr)
        else:
            return [ self._visit(expr),  self._depth_first_walk(expr.left()), self._depth_first_walk(expr.right()) ]
            
    def _visit(self, expr):
        if isinstance(expr, smoek.core.expression.BinaryExprNode):
            return expr.operation()
        else:
            return expr.to_string()

def to_list(expr):
    return ExpressionToList().expression_to_list(expr)

