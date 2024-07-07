from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
import smoek.core.expr.nodes
from smoek.core.expr.nodes import ExprNode
import smoek.core.expr.functions
import smoek.core.model.expressions


native_types = {float, int}


#class Walker(ABC):
#    def __init__(self) -> None:
#        self._stack = []
#
#    @abstractmethod
#    def enter_node(self, node: ExprNode):
#        pass
#
#    @abstractmethod
#    def exit_node(self, node: ExprNode):
#        pass
#
#    def walk(self, expr: ExprNode):
#        self._stack = [expr]
#        prefix = []
#        while len(self._stack) > 0:
#            node = self._stack.pop()
#            prefix.append(node)
#            self.enter_node(node)
#            if not node.is_leaf():
#                self._stack.extend(reversed(node.args()))
#        for node in reversed(prefix):
#            self.exit_node(node)


T = TypeVar("T")


class BottomUpDepthFirstExpressionWalker(Generic[T]):
    def __init__(self):
        self._depth = 0
        self._stack: List[T] = []

    def _walk(self, expr: ExprNode, **kwargs):
        assert self._depth == 0
        self._depth_first_walk(expr, *kwargs)
        assert self._depth == 0

    def _depth_first_walk(self, expr: ExprNode, **kwargs):
        assert expr is not None
        if isinstance(expr, smoek.core.expr.nodes.BinaryExprNode):
            self._depth += 1
            self._depth_first_walk(expr.left, *kwargs)
            self._depth_first_walk(expr.right, *kwargs)
            self._depth -= 1
            self._visit(expr, *kwargs)
        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            self._depth += 1
            self._depth_first_walk(expr.arg, *kwargs)
            self._depth -= 1
            self._visit(expr, *kwargs)
        elif isinstance(expr, smoek.core.expr.functions.SumExprNode):
            self._depth += 1
            self._depth_first_walk(expr._expr, *kwargs)
            self._depth -= 1
            self._visit(expr, *kwargs)
        elif isinstance(expr, smoek.core.expr.functions.ProdExprNode):
            self._depth += 1
            self._depth_first_walk(expr._expr, *kwargs)
            self._depth -= 1
            self._visit(expr, *kwargs)
        elif isinstance(expr, smoek.core.model.expressions.Expression):
            self._depth += 1
            self._depth_first_walk(expr._expr, *kwargs)
            self._depth -= 1
            self._visit(expr, *kwargs)
        elif isinstance(expr, smoek.core.expr.nodes.ExprLeaf):
            self._visit(expr, *kwargs)
        else:
            raise NotImplementedError(
                f"Expression node {expr} of type {type(expr)} not supported in BottomUpDepthFirstExpressionWalker"
            )

    def _visit(self, expr: ExprNode, **kwargs):
        raise NotImplementedError(
            "BottomUpDepthFirstExpressionWalker._visit needs to be implemented by the derived class"
        )

    def walk(self, expr, **kwargs) -> T:
        assert self._stack == []
        self._walk(expr, *kwargs)
        ret = self._stack.pop()
        assert self._stack == []
        return ret


class ExpressionToStringWalker(BottomUpDepthFirstExpressionWalker[str]):
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
        if isinstance(expr, smoek.core.expr.nodes.BinaryExprNode):
            right = self._stack.pop()
            left = self._stack.pop()
            ret = f"{left} {expr.operation} {right}"
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            arg = self._stack.pop()
            ret = f"{expr.operation}({arg})"
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr.nodes.ExprLeaf):
            ret = f"{expr.to_string()}"
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr.functions.SumExprNode):
            body = self._stack.pop()
            ret = f"sum({expr._forall.to_string()}, {body})"
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr.functions.ProdExprNode):
            body = self._stack.pop()
            ret = f"prod({expr._forall.to_string()}, {body})"
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.model.expressions.Expression):
            body = self._stack.pop()
            ret = f"({body})"
            self._stack.append(ret)
        else:
            raise NotImplementedError(
                f"Expression node {expr} of type {type(expr)} not supported in ExpressionToStringWalker"
            )


class ExpressionToListWalker(BottomUpDepthFirstExpressionWalker[List]):
    def __init__(self):
        super().__init__()
        self._stack = []

    def expression_to_list(self, expr):
        assert self._stack == []
        self._walk(expr)
        ret = self._stack.pop()
        assert self._stack == [], "Expected empty stack: " + str(self._stack)
        return ret

    def _visit(self, expr):
        if isinstance(expr, smoek.core.expr.nodes.BinaryExprNode):
            right = self._stack.pop()
            left = self._stack.pop()
            ret = [str(expr.operation), left, right]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            arg = self._stack.pop()
            ret = [str(expr.operation), arg]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr.functions.SumExprNode):
            body = self._stack.pop()
            ret = ["sum", expr._forall.to_string(), body]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr.functions.ProdExprNode):
            body = self._stack.pop()
            ret = ["prod", expr._forall.to_string(), body]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.model.expressions.Objective):
            body = self._stack.pop()
            if expr.sense():
                ret = ["minimize"] + body
            else:
                ret = ["maximize"] + body
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.model.expressions.Expression):
            body = self._stack.pop()
            ret = [body]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.expr.nodes.ExprLeaf):
            ret = expr.to_string()
            self._stack.append(ret)
        else:
            raise NotImplementedError(
                f"Expression node {expr} of type {type(expr)} not supported in ExpressionToListWalker"
            )


def expr_to_list(expr):
    return ExpressionToListWalker().expression_to_list(expr)


def expr_to_string(expr):
    return ExpressionToStringWalker().expression_to_string(expr)


class CollectLeafInfo(BottomUpDepthFirstExpressionWalker[List]):
    def __init__(self):
        super().__init__()
        self._info = {}
        self._info = {'variables':{}, 'index_sets':{}, 'parameters':{}, 'data':{}, 'expressions':{}}

    def walk(self, expr):
        self._walk(expr)
        return self._info

    def _visit(self, expr):
        if isinstance(expr, smoek.core.expr.nodes.ComponentIndicesNode):
            # Indexed component
            if isinstance(expr._component, smoek.core.model.data_components.Parameter):
                self._info['parameters'][expr._component.name()] = expr._component
            elif isinstance(expr._component, smoek.core.model.data_components.Data):
                self._info['data'][expr._component.name()] = expr._component
            elif isinstance(expr._component, smoek.core.model.var_components.IndexedVariable):
                self._info['variables'][expr._component.name()] = expr._component
            elif isinstance(expr._component, smoek.core.model.expressions.Expression):
                self._info['expressions'][expr._component.name()] = expr._component

            for indexset in expr._component._index_sets():
                self._info['index_sets'][indexset.name()] = indexset

        elif isinstance(expr, smoek.core.model.data_components.Parameter):
            # Unindexed parameter
            self._info['parameters'][expr.name()] = expr

        elif isinstance(expr, smoek.core.model.data_components.Data):
            # Unindexed data
            self._info['data'][expr.name()] = expr

        elif isinstance(expr, smoek.core.model.var_components.ScalarVariable):
            # Unindexed variable
            self._info['variables'][expr.name()] = expr


def collect_expr_leaves(expr):
    return CollectLeafInfo().walk(expr)


def model_to_dict(model):
    ans = {'objectives': {}, 'constraints':{}, 'variables':{}, 'index_sets':{}, 'parameters':{}, 'data':{}, 'expressions':{}}
    info = collect_expr_leaves(model.objective)
    for component in info:
        for k,v in info[component].items():
            ans[component][k] = str(v)
    ans['objectives'][model.objective.name()] = expr_to_list(model.objective)

    for c in model.constraints:
        info = collect_expr_leaves(c.expr())
        for component in info:
            for k,v in info[component].items():
                ans[component][k] = str(v)
        ans['constraints'][c.name()] = expr_to_list(c.expr())
    return ans


class ExpressionDepthWalker(BottomUpDepthFirstExpressionWalker):

    def __init__(self):
        super().__init__()
        self._max_depth = 0

    def _visit(self, expr):
        if self._depth > self._max_depth:
            self._max_depth = self._depth


def get_expression_depth(expr):
    walker = ExpressionDepthWalker()
    walker._walk(expr)
    return walker._max_depth
