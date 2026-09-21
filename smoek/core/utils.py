from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from munch import Munch
import smoek.core.expr.nodes
from smoek.core.expr.nodes import ExprNode
import smoek.core.expr.functions
import smoek.core.model.expressions

native_types = {float, int}


# class Walker(ABC):
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
        elif isinstance(expr, smoek.core.expr.nodes.InequalityExprNode):
            self._depth += 1
            self._depth_first_walk(expr.left, *kwargs)
            self._depth_first_walk(expr.body, *kwargs)
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
        elif isinstance(expr, smoek.core.model.expressions.Objective):
            self._depth += 1
            self._depth_first_walk(expr._expr, *kwargs)
            self._depth -= 1
            self._visit(expr, *kwargs)
        elif isinstance(expr, smoek.core.model.constr_components.Constraint):
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
        elif isinstance(expr, smoek.core.expr.nodes.InequalityExprNode):
            right = self._stack.pop()
            body = self._stack.pop()
            left = self._stack.pop()
            ret = f"{left} <= {body} <= {right}"
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
        elif isinstance(expr, smoek.core.expr.nodes.InequalityExprNode):
            right = self._stack.pop()
            body = self._stack.pop()
            left = self._stack.pop()
            ret = ["<=", left, body, right]
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
            if type(body) is not list:
                body = [body]
            if expr.sense():
                ret = ["minimize"] + body
            else:
                ret = ["maximize"] + body
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.model.expressions.Expression):
            body = self._stack.pop()
            ret = [body]
            self._stack.append(ret)
        elif isinstance(expr, smoek.core.model.constr_components.Constraint):
            body = self._stack.pop()
            ret = body
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

    def walk(self, expr, info_dict=None):
        if info_dict is not None:
            self._info = info_dict
        self._walk(expr)
        return self._info

    def _visit(self, expr):
        if isinstance(expr, smoek.core.expr.nodes.ComponentIndicesNode):
            # Indexed component
            if expr._component.name() in self._info:
                return

            self._visit(expr._component)
            for indexset in expr._component._index_sets():
                self._info[indexset.name()] = Munch(
                    name=indexset.name(),
                    id=indexset._id,
                    dependencies=indexset._dependencies(),
                    type="index_set",
                    object=indexset,
                )
            for index in expr.indices:
                if isinstance(index, smoek.core.model.components.Index):
                    self._info[index.name()] = Munch(
                        name=index.name(),
                        id=index._id,
                        dependencies=[],
                        type="index",
                        object=index,
                    )

        elif isinstance(expr, smoek.core.model.data_components.Parameter):
            # Unindexed parameter
            name = expr.name()
            if name in self._info:
                return
            self._info[name] = Munch(
                name=name,
                id=expr._id,
                dependencies=expr._dependencies(),
                type="parameter",
                object=expr,
            )

        elif isinstance(expr, smoek.core.model.data_components.Data):
            # Unindexed data
            name = expr.name()
            if name in self._info:
                return
            self._info[name] = Munch(
                name=name,
                id=expr._id,
                dependencies=expr._dependencies(),
                type="data",
                object=expr,
            )

        elif isinstance(expr, smoek.core.model.var_components.ScalarVariable) or isinstance(
            expr, smoek.core.model.var_components.IndexedVariable
        ):
            # Unindexed variable
            name = expr.name()
            if name in self._info:
                return
            self._info[name] = Munch(
                name=name,
                id=expr._id,
                dependencies=expr._dependencies(),
                type="variable",
                object=expr,
            )

        elif isinstance(expr, smoek.core.model.expressions.Expression):
            # Unindexed expression
            name = expr.name()
            if name in self._info:
                return
            self._info[name] = Munch(
                name=name,
                id=expr._id,
                dependencies=expr._dependencies(),
                type="expression",
                object=expr,
            )


def collect_expr_leaves(expr, info_dict=None):
    return CollectLeafInfo().walk(expr, info_dict)


def collect_info(model):
    if model.objective:
        info = collect_expr_leaves(model.objective)
        for c in model.constraints:
            info = collect_expr_leaves(c.expr(), info)

        o = model.objective
        info[o.name()] = Munch(
            name=o.name(),
            id=o._id,
            dependencies=o._dependencies(),
            type="objective",
            object=o,
        )
    else:
        info = {}

    for c in model.constraints:
        info[c.name()] = Munch(
            name=c.name(),
            id=c._id,
            dependencies=c._dependencies(),
            type="constraint",
            object=c,
        )
    return info


#
# This function returns an ordering of model components that is based on the
# order of component creation.  This is *often* but not always a valid order for
# initializing model components.
#
# TODO: Check this ordering using the 'dependencies' information
#
def valid_order(info):
    names = [v.name for v in info.values()]
    names.sort(key=lambda x: info[x].id)
    return names


def model_to_dict(model):
    info = collect_info(model)

    ans = {
        "objectives": {},
        "constraints": {},
        "variables": {},
        "index_sets": {},
        "parameters": {},
        "data": {},
        "expressions": {},
    }
    for k, v in info.items():
        if v.type == "parameter":
            ans["parameters"][k] = str(v.object)
        elif v.type == "data":
            ans["data"][k] = str(v.object)
        elif v.type == "variable":
            ans["variables"][k] = str(v.object)
        elif v.type == "expression":
            ans["expressions"][k] = str(v.object)
        elif v.type == "index_set":
            ans["index_sets"][k] = str(v.object)
        elif v.type == "objective":
            ans["objectives"][k] = expr_to_list(v.object)
        elif v.type == "constraint":
            ans["constraints"][k] = expr_to_list(v.object)

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
