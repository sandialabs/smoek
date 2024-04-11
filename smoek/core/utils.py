import smoek.core.expr_components
import smoek.core.functions

class BottomUpDepthFirstExpressionWalker(object):
    def __init__(self):
        self._depth = 0

    def _walk(self, expr):
        assert self._depth == 0
        self._depth_first_walk(expr)
        assert self._depth == 0
        
    def _depth_first_walk(self, expr):
        assert expr is not None
        if isinstance(expr, smoek.core.expr_components.ExprLeaf):
            self._visit(expr)
        elif isinstance(expr, smoek.core.expr_components.BinaryExprNode):
            self._depth += 1
            self._depth_first_walk(expr.left)
            self._depth_first_walk(expr.right)
            self._depth -= 1
            self._visit(expr)
        elif isinstance(expr, smoek.core.functions.UnaryExprNode):
            self._depth += 1
            self._depth_first_walk(expr.arg)
            self._depth -= 1
            self._visit(expr)
        elif isinstance(expr, smoek.core.functions.SumExprNode):
            self._depth += 1
            self._depth_first_walk(expr._expr)
            self._depth -= 1
            self._visit(expr)
        elif isinstance(expr, smoek.core.functions.ProdExprNode):
            self._depth += 1
            self._depth_first_walk(expr._expr)
            self._depth -= 1
            self._visit(expr)
        elif isinstance(expr, smoek.core.expressions.Expression):
            self._depth += 1
            self._depth_first_walk(expr.expr)
            self._depth -= 1
            self._visit(expr)
        else:
            raise NotImplementedError(f'Expression node {expr} of type {type(expr)} not supported in BottomUpDepthFirstExpressionWalker')

    def _visit(self, expr):
        raise NotImplementedError('BottomUpDepthFirstExpressionWalker._visit needs to be implemented by the derived class')



class ExpressionToStringWalker(BottomUpDepthFirstExpressionWalker):
    def __init__(self):
        super().__init__()
        self._stack = []

    def expression_to_string(self, expr):
        assert self._stack == []
        self._walk(expr)
        ret = self._stack.pop(0)
        assert self._stack == []
        return ret

    def _visit(self, expr):
        if isinstance(expr, smoek.core.expr_components.BinaryExprNode):
            right = self._stack.pop()
            left = self._stack.pop()
            ret = f'{left} {expr.operation} {right}'
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.functions.UnaryExprNode):
            arg = self._stack.pop()
            ret = f'{expr.operation}({arg})'
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr_components.ExprLeaf):
            ret = f'{expr.to_string()}'
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.functions.SumExprNode):
            body = self._stack.pop()
            ret = f'sum({expr._forall.to_string()}, {body})'
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.functions.ProdExprNode):
            body = self._stack.pop()
            ret = f'prod({expr._forall.to_string()}, {body})'
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expressions.Expression):
            body = self._stack.pop()
            ret = f'({body})'
            self._stack.append(ret)
        else:
            raise NotImplementedError(f'Expression node {expr} of type {type(expr)} not supported in ExpressionToStringWalker')
        


class ExpressionToListWalker(BottomUpDepthFirstExpressionWalker):
    def __init__(self):
        super().__init__()
        self._stack = []

    def expression_to_list(self, expr):
        assert self._stack == []
        self._walk(expr)
        ret = self._stack.pop()
        assert self._stack == []
        return ret

    def _visit(self, expr):
        if isinstance(expr, smoek.core.expr_components.BinaryExprNode):
            right = self._stack.pop()
            left = self._stack.pop()
            ret = [expr.operation, left, right]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.functions.UnaryExprNode):
            arg = self._stack.pop()
            ret = [expr.operation, arg]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr_components.ExprLeaf):
            ret = expr.to_string()
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.functions.SumExprNode):
            body = self._stack.pop()
            ret = ['sum', expr._forall.to_string(), body]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.functions.ProdExprNode):
            body = self._stack.pop()
            ret = ['prod', expr._forall.to_string(), body]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expressions.Expression):
            body = self._stack.pop()
            ret = [body]
            self._stack.append(ret)
        else:
            raise NotImplementedError(f'Expression node {expr} of type {type(expr)} not supported in ExpressionToListWalker')


def expr_to_list(expr):
    return ExpressionToListWalker().expression_to_list(expr)

def expr_to_string(expr):
    return ExpressionToStringWalker().expression_to_string(expr)





# class ExpressionPrinter:
#     def __init__(self):
#         self._depth = 0

#     def expression_to_string(self, expr):
#         assert self._depth == 0
#         self._ret = ''
        
#         self._depth_first_walk(expr)
#         assert self._depth == 0

#         self._ret += '\n'
#         ret = self._ret
#         self._ret = None
#         return ret

#     def print_expression(self, expr):
#         print(self.expression_to_string(expr))
        
#     def _depth_first_walk(self, expr):
#         if isinstance(expr, smoek.core.expr_components.ExprLeaf):
#             self._visit(expr)
#         else:
#             self._visit(expr)
#             self._depth += 1
#             self._depth_first_walk(expr.left)
#             self._depth_first_walk(expr.right)
#             self._depth -= 1
            
#     def _visit(self, expr):
#         if isinstance(expr, smoek.core.expr_components.BinaryExprNode):
#             self._ret += '\n{}{}'.format(' '*self._depth*3, expr.operation)
#         else:
#             self._ret += '\n{}{}'.format(' '*self._depth*3, expr.to_string())

# class ExpressionToString:
#     def expression_to_string(self, expr):
#         return self._depth_first_walk(expr)

#     def _depth_first_walk(self, expr):
#         # TODO: deal with parentheses
#         if isinstance(expr, smoek.core.expr_components.ExprLeaf):
#             return f'{self._visit(expr)}'
#         elif isinstance(expr, smoek.core.expr_components.BinaryExprNode):
#             return  f'({self._depth_first_walk(expr.left)} {self._visit(expr)} {self._depth_first_walk(expr.right)})'
#         elif isinstance(expr, smoek.core.functions.UnaryExprNode):
#             return f'{self._visit(expr)}({self._depth_first_walk(expr.arg)})'
#         elif isinstance(expr, smoek.core.functions.SumExprNode):
#             return f'sum({self._depth_first_walk(expr._expr)}, {expr._forall.to_string()})'
#         # TODO: case for Expression object
            
#     def _visit(self, expr):
#         if isinstance(expr, smoek.core.expr_components.BinaryExprNode) or isinstance(expr, smoek.core.functions.UnaryExprNode):
#             return expr.operation
#         elif isinstance(expr, smoek.core.expr_components.ExprLeaf):
#             return expr.to_string()

# class ExpressionToList:
#     def expression_to_list(self, expr):
#         return self._depth_first_walk(expr)

#     def _depth_first_walk(self, expr):
#         if isinstance(expr, smoek.core.expr_components.ExprLeaf):
#             return f'{self._visit(expr)}'
#         elif isinstance(expr, smoek.core.expr_components.BinaryExprNode):
#             return  [self._depth_first_walk(expr.left), self._visit(expr), self._depth_first_walk(expr.right)]
#         elif isinstance(expr, smoek.core.functions.UnaryExprNode):
#             return [self._visit(expr), self._depth_first_walk(expr.arg)]
#         elif isinstance(expr, smoek.core.functions.SumExprNode):
#             return [f'sum({expr._forall.to_string()})', self._depth_first_walk(expr._expr)]
            
#     def _visit(self, expr):
#         if isinstance(expr, smoek.core.expr_components.BinaryExprNode) or isinstance(expr, smoek.core.functions.UnaryExprNode):
#             return expr.operation
#         elif isinstance(expr, smoek.core.expr_components.ExprLeaf):
#             return expr.to_string()
        