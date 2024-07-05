from pyomo.common.collections import ComponentMap
from smoek.core.expr.nodes import ExprNode, ExpressionType
from smoek.core.expr.functions import log, exp, sin, cos, tan
from smoek.core.utils import Walker


def diff_add(node, der_map):
    for arg in node.args():
        if arg not in der_map:
            der_map[arg] = 0
        der_map[arg] += der_map[node]


def diff_sub(node, der_map):
    for arg in node.args():
        if arg not in der_map:
            der_map[arg] = 0
    der_map[node.left] += der_map[node]
    der_map[node.right] -= der_map[node]


def diff_mul(node, der_map):
    for arg in node.args():
        if arg not in der_map:
            der_map[arg] = 0
    der_map[node.left] += der_map[node] * node.right
    der_map[node.right] += der_map[node] * node.left


def diff_div(node, der_map):
    for arg in node.args():
        if arg not in der_map:
            der_map[arg] = 0
    der_map[node.left] += der_map[node] / node.right
    der_map[node.right] -= der_map[node] * node.left / node.right**2


def diff_pow(node, der_map):
    for arg in node.args():
        if arg not in der_map:
            der_map[arg] = 0
    der_map[node.left] += der_map[node] * node.right * node.left ** (node.right - 1)
    der_map[node.right] += der_map[node] * node.left**node.right * log(node.left)


def diff_neg(node, der_map):
    if node.arg not in der_map:
        der_map[node.arg] = 0
    der_map[node.arg] -= der_map[node]


def diff_exp(node, der_map):
    if node.arg not in der_map:
        der_map[node.arg] = 0
    der_map[node.arg] += der_map[node] * exp(node.arg)


def diff_log(node, der_map):
    if node.arg not in der_map:
        der_map[node.arg] = 0
    der_map[node.arg] += der_map[node] / node.arg


def diff_sin(node, der_map):
    if node.arg not in der_map:
        der_map[node.arg] = 0
    der_map[node.arg] += der_map[node] * cos(node.arg)


def diff_cos(node, der_map):
    if node.arg not in der_map:
        der_map[node.arg] = 0
    der_map[node.arg] -= der_map[node] * sin(node.arg)


def diff_tan(node, der_map):
    if node.arg not in der_map:
        der_map[node.arg] = 0
    der_map[node.arg] += der_map[node] / cos(node.arg) ** 2


def diff_indexed_component(node, der_map):
    pass


def diff_constant(node, der_map):
    pass


diff_map = {}
diff_map[ExpressionType.add] = diff_add
diff_map[ExpressionType.sub] = diff_sub
diff_map[ExpressionType.mul] = diff_mul
diff_map[ExpressionType.div] = diff_div
diff_map[ExpressionType.pow] = diff_pow
diff_map[ExpressionType.neg] = diff_neg
diff_map[ExpressionType.exp] = diff_exp
diff_map[ExpressionType.log] = diff_log
diff_map[ExpressionType.sin] = diff_sin
diff_map[ExpressionType.cos] = diff_cos
diff_map[ExpressionType.tan] = diff_tan
diff_map[ExpressionType.indexed_component] = diff_indexed_component
diff_map[ExpressionType.constant] = diff_constant


class ReverseSDWalker(Walker):
    def __init__(self) -> None:
        super().__init__()
        self._ders = ComponentMap()

    def enter_node(self, node: ExprNode):
        diff_map[node.etype()](node, self._ders)

    def exit_node(self, node: ExprNode):
        pass

    def walk(self, expr: ExprNode):
        self._ders[expr] = 1
        super().walk(expr)
        return self._ders
