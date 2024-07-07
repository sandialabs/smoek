import pyomo.environ as pyo
from smoek.core.util import BottomUpDepthFirstExpressionWalker, collect_info, valid_order


class SmoekToPyomoWalker(BottomUpDepthFirstExpressionWalker[str]):
    def __init__(self):
        super().__init__()
        self._stack = []

    def walk(self, expr, decl):
        self._decl = decl
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
            elif expr.operation == "sin":
                ret = pyo.sin(arg)
            elif expr.operation == "cos":
                ret = pyo.cos(arg)
            elif expr.operation == "tan":
                ret = pyo.tan(arg)
            elif expr.operation == "sqrt":
                ret = pyo.sqrt(arg)
            else:
                ret = None  # ERROR
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.model.var_components.ScalarVariable):
            self._stack.append( self._decl(expr.name()) )

        elif isinstance(expr, smoek.core.model.data_components.Parameter):
            self._stack.append( self._decl(expr.name()) )

        elif isinstance(expr, smoek.core.model.data_components.Data):
            self._stack.append( self._decl(expr.name()) )

        elif isinstance(expr, smoek.core.expr.nodes.ComponentIndicesNode)
            if isinstance(expr._component, smoek.core.model.var_components.ScalarVariable):
                

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


def to_pyomo(expr, decl={}):
    return SmoekToPyomoWalker().walk(expr, decl)


def generate(*, model=None, data=None):
    """
    Returns a Pyomo concrete model instance generated from a smoek model
    """

    M = pyo.ConcreteModel(model.name)

    components = []
    parameters = {}

    info = collect_info(model)
    order = valid_order(info)
    print("HERE", order)

    pyomo_decl = {}
    for name in order:
        component = info[name]
        pyo_component = None

        if component.type == "index_set":
            pyo_component = pyo.Set(initialize=component.object.data())

        elif component.type == "parameter":
            if component.object.is_indexed():
                #setattr(M, component.name, pyo.Param(initialize=component.object.data(), mutable=True))
                pass
            else:
                pyo_component = pyo.Param(initialize=to_pyomo(component.object.value(), pyomo_decl), mutable=True)
    
        elif component.type == "data":
            if component.object.is_indexed():
                #setattr(M, component.name, pyo.Param(initialize=component.object.data(), mutable=False))
                pass
            else:
                pyo_component = pyo.Param(initialize=to_pyomo(component.object.value(), pyomo_decl), mutable=False)
    
        elif component.type == "expression":
            if component.object.is_indexed():
                #setattr(M, component.name, pyo.Expression(initialize=component.object.data()), mutable=False)
                pass
            else:
                #setattr(M, component.name, pyo.Expression(expr=to_pyomo(component.object.expr()), mutable=False))
                pass
   
        elif component.type == "objective":
            sense = pyo.Objective.minimize if component.object.sense() else pyo.Objective.maximize
            if component.object.is_indexed():
                #setattr(M, component.name, pyo.Expression(initialize=component.object.data()), mutable=False)
                pass
            else:
                pyo_component = pyo.Objective(expr=to_pyomo(component.object.expr(), pyomo_decl), sense=sense)

        elif component.type == "constraint":
            if component.object.is_indexed():
                #setattr(M, component.name, pyo.Expression(initialize=component.object.data()), mutable=False)
                pass
            else:
                pyo_component = pyo.Constraint(expr=to_pyomo(component.object.expr(), pyomo_decl))

        if pyo_component is not None:
            setattr(M, component.name, pyo_component)
            pyomo_decl[component.name] = pyo_component

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
