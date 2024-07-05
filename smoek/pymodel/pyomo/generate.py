import pyomo.environ as pyo
from smoek.core.util import BottomUpDepthFirstExpressionWalker


class SmoekToPyomoWalker(BottomUpDepthFirstExpressionWalker[str]):
    def __init__(self):
        super().__init__()
        self._stack = []

    def to_pyomo(self, expr):
        assert self._stack == []
        self._walk(expr)
        ret = self._stack.pop(0)
        assert self._stack == []
        return ret

    def _visit(self, expr):
        if isinstance(expr, smoek.core.expr.nodes.BinaryExprNode):
            right = self._stack.pop()
            left = self._stack.pop()
            if expr.operation == "+":
                ret = left + right
            elif expr.operation == "-":
                ret = left - right
            elif expr.operation == "*":
                ret = left * right
            elif expr.operation == "/":
                ret = left / right
            else:
                ret = None  # ERROR
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            arg = self._stack.pop()
            if expr.operation == "log":
                ret = pyo.log(arg)
            else:
                ret = None  # ERROR
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

        elif isinstance(expr, smoek.core.expressions.Expression):
            body = self._stack.pop()
            ret = f"({body})"
            self._stack.append(ret)

        else:
            raise NotImplementedError(
                f"Expression node {expr} of type {type(expr)} not supported in ExpressionToStringWalker"
            )


def to_pyomo(expr, parameters=None):
    print(expr_to_list(expr))


def generate(*, model=None, data=None):
    """
    Returns a Pyomo concrete model instance generated from a smoek model
    """

    M = pyo.ConcreteModel(model.name)

    components = []
    parameters = {}

    #
    # Objective
    #
    if model.objective.sense:
        sense = pyo.minimize
    else:
        sense = pyo.maximize
    if model.objective.is_scalar():
        components.append(
            [
                model.objective.name,
                pyo.Objective(
                    expr=to_pyomo(model.objective.expr, parameters), sense=sense
                ),
            ]
        )
    else:
        print("Indexed objectives not supported yet")

    #
    # Constraints
    #
    for con in model.constraints:
        if con.is_scalar():
            components.append(
                [con.name, pyo.Constraint(expr=to_pyomo(con.expr, parameters))]
            )
        else:
            index_set = con.index_set()

    return M
