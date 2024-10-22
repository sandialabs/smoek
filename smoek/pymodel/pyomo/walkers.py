import smoek.core.expr.nodes
from smoek.core.expr.nodes import ExpressionType
from smoek.core.model.var_components import (
    Reals,
    PositiveReals,
    NegativeReals,
    Binary,
    Integers,
    PositiveIntegers,
    NegativeIntegers,
    NonNegativeIntegers,
    NonPositiveIntegers,
)
import smoek.core.expr.functions
from smoek.core.utils import (
    BottomUpDepthFirstExpressionWalker,
    collect_info,
    valid_order,
)

try:
    import pyomo.environ as pyo

    pyomo_available = True
except:  # pragma: nocover
    pyomo_available = False

if pyomo_available:
    domain = {
        Reals.id: pyo.Reals,
        PositiveReals.id: pyo.PositiveReals,
        NegativeReals.id: pyo.NegativeReals,
        Binary.id: pyo.Binary,
        Integers.id: pyo.Integers,
        PositiveIntegers.id: pyo.PositiveIntegers,
        NegativeIntegers.id: pyo.NegativeIntegers,
        NonNegativeIntegers.id: pyo.NonNegativeIntegers,
        NonPositiveIntegers.id: pyo.NonPositiveIntegers,
    }
    unary = {
        "sin": pyo.sin,
        "cos": pyo.cos,
        "tan": pyo.tan,
        "asin": pyo.asin,
        "acos": pyo.acos,
        "atan": pyo.atan,
        "log": pyo.log,
        "log10": pyo.log10,
    }


def _name(name):
    return name.replace("[", "_").replace("]", "_")


class SmoekToPyomoExprWalker(BottomUpDepthFirstExpressionWalker[str]):
    def __init__(self):
        super().__init__()
        self._stack = []

    def walk(self, expr, decl, model):
        self._decl = decl
        self._model = model
        assert self._stack == []
        self._walk(expr)
        ret = self._stack.pop(0)
        assert self._stack == []
        return ret

    def _visit(self, expr):
        if isinstance(expr, smoek.core.expr.nodes.BinaryExprNode):
            right = self._stack.pop()
            left = self._stack.pop()
            if expr.operation == ExpressionType.pow:
                ret = left**right
            elif expr.operation == ExpressionType.eq:
                ret = left == right
            elif expr.operation == ExpressionType.leq:
                ret = left <= right
            elif expr.operation == ExpressionType.geq:
                ret = left >= right
            elif expr.operation == ExpressionType.add:
                ret = left + right
            elif expr.operation == ExpressionType.sub:
                ret = left - right
            elif expr.operation == ExpressionType.mul:
                ret = left * right
            elif expr.operation == ExpressionType.div:
                ret = left / right
            else:
                self._stack.append(None)
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.nodes.InequalityExprNode):
            right = self._stack.pop()
            body = self._stack.pop()
            left = self._stack.pop()
            ret = pyo.inequality(left, body, right)
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            if expr.operation == "neg":
                ret = self._stack.pop()
                self._stack.append(-ret)
            else:
                arg = self._stack.pop()
                ret = unary[expr.operation](arg)
                self._stack.append(ret)

        elif isinstance(expr, smoek.core.model.var_components.ScalarVariable):
            self._stack.append(getattr(self._model, expr.name()))

        elif isinstance(expr, smoek.core.model.data_components.Parameter):
            self._stack.append(getattr(self._model, expr.name()))

        # elif isinstance(expr, smoek.core.model.data_components.Data):
        #    self._stack.append( expr.name() )

        elif isinstance(expr, smoek.core.expr.nodes.ComponentIndicesNode):
            indices = [str(index) for index in expr._indices]
            ret = f'{self._model}.{expr._component.name()}[{",".join(indices)}]'
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.nodes.NumberWrapper):
            self._stack.append(expr.value)

        elif isinstance(expr, smoek.core.expr.functions.SumExprNode):
            body = self._stack.pop()
            ret = f"sum({body}"
            for pair in expr._forall._index_set_pairs:
                index = str(pair.index)
                index_set = pair.set.name()
                ret += f" for {index} in {self._model}.{index_set}"
            ret += ")"
            self._stack.append(ret)

        # elif isinstance(expr, smoek.core.expressions.Expression):
        #    body = self._stack.pop()
        #    ret = f"({body})"
        #    self._stack.append(ret)

        else:  # pragma: nocover
            raise NotImplementedError(
                f"Expression node {expr} of type {type(expr)} not supported in ExpressionToStringWalker"
            )


class SmoekToPyomoStringWalker(BottomUpDepthFirstExpressionWalker[str]):
    def __init__(self):
        super().__init__()
        self._stack = []

    def walk(self, expr, decl, model):
        self._decl = decl
        self._model = model
        assert self._stack == []
        self._walk(expr)
        ret = self._stack.pop(0)
        assert self._stack == []
        return ret

    def _visit(self, expr):
        if isinstance(expr, smoek.core.expr.nodes.BinaryExprNode):
            right = self._stack.pop()
            left = self._stack.pop()
            if expr.operation == ExpressionType.pow:
                ret = f"({left}) ** ({right})"
            elif expr.operation in [
                ExpressionType.eq,
                ExpressionType.leq,
                ExpressionType.geq,
            ]:
                ret = f"{left} {expr.operation} {right}"
            else:
                if isinstance(
                    expr._right, smoek.core.expr.nodes.BinaryExprNode
                ) and expr._right.operation in [
                    ExpressionType.add,
                    ExpressionType.sub,
                    ExpressionType.mul,
                    ExpressionType.div,
                ]:
                    right = f"({right})"
                if isinstance(
                    expr._left, smoek.core.expr.nodes.BinaryExprNode
                ) and expr._left.operation in [
                    ExpressionType.add,
                    ExpressionType.sub,
                    ExpressionType.mul,
                    ExpressionType.div,
                ]:
                    left = f"({left})"
                ret = f"{left} {expr.operation} {right}"
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.nodes.InequalityExprNode):
            right = self._stack.pop()
            body = self._stack.pop()
            left = self._stack.pop()
            ret = f"pyo.inequality({left}, {body}, {right})"
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            if expr.operation == "neg":
                arg = self._stack.pop()
                if isinstance(
                    expr._arg, smoek.core.expr.nodes.BinaryExprNode
                ) and expr._arg.operation in [
                    ExpressionType.add,
                    ExpressionType.sub,
                    ExpressionType.mul,
                    ExpressionType.div,
                ]:
                    ret = f"(-({arg}))"
                else:
                    ret = f"(-{arg})"
                self._stack.append(ret)
            else:
                arg = self._stack.pop()
                ret = f"pyo.{expr.operation}({arg})"
                self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.nodes.ComponentIndicesNode):
            indices = [str(index) for index in expr._indices]
            ret = f'{self._model}.{expr._component.name()}[{",".join(indices)}]'
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.nodes.ExprLeaf):
            if expr.is_component():
                ret = f"{self._model}.{expr.to_string()}"
            else:
                ret = f"{expr.to_string()}"
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.functions.SumExprNode):
            body = self._stack.pop()
            ret = f"sum({body}"
            for pair in expr._forall._index_set_pairs:
                index = str(pair.index)
                index_set = pair.set.name()
                ret += f" for {index} in {self._model}.{index_set}"
            ret += ")"
            self._stack.append(ret)

        # elif isinstance(expr, smoek.core.expressions.Expression):
        #    body = self._stack.pop()
        #    ret = f"({body})"
        #    self._stack.append(ret)

        else:  # pragma: nocover
            raise NotImplementedError(
                f"Expression node {expr} of type {type(expr)} not supported in ExpressionToStringWalker"
            )


# TODO - Can we eliminate this function?
def to_pyomo(expr, decl={}, model=None):
    return SmoekToPyomoExprWalker().walk(expr, decl, model)


def to_pyomo_str(expr, decl={}):
    return SmoekToPyomoStringWalker().walk(expr, decl, "m_")


def generate(*, model=None, data=None):
    """
    Generate a Pyomo model described by smoek.
    """
    if not pyomo_available:  # pragma: nocover
        return None

    if data is None:
        data = {}

    info = collect_info(model)
    order = valid_order(info)

    M = pyo.ConcreteModel()

    for name in order:
        component = info[name]
        pyomo_str = None

        if component.type == "index":
            continue

        elif component.type == "index_set":
            if isinstance(component.object, smoek.core.model.set_components.RangeSet):
                setattr(
                    M,
                    component.name,
                    pyo.RangeSet(0, to_pyomo(component.object._N, model=M)),
                )
            elif isinstance(
                component.object, smoek.core.model.set_components.SequenceSet
            ):
                setattr(
                    M,
                    component.name,
                    pyo.RangeSet(
                        to_pyomo(component.object._start, model=M),
                        to_pyomo(component.object._stop, model=M),
                    ),
                )
            else:

                def set_(m):
                    return data[component.name]

                setattr(M, component.name, pyo.Set(initialize=set_))

        elif component.type == "parameter" or component.type == "data":
            index_sets = [
                getattr(M, iset.name()) for iset in component.object._index_sets()
            ]

            kwargs = {}
            kwargs["mutable"] = component.type == "parameter"
            kwargs["domain"] = pyo.Reals
            # print("HERE", component.name, type(data), data)
            if component.name in data:
                kwargs["initialize"] = data[component.name]
            elif isinstance(
                component.object.value(), smoek.core.expr.nodes.NumberWrapper
            ):
                kwargs["initialize"] = component.object.value().value
            elif isinstance(
                component.object.value(), smoek.core.expr.nodes.DataWrapper
            ):
                kwargs["initialize"] = component.object.value().value
            elif component.object.value():
                if component.object.is_indexed():
                    indices = [i.name() for i in component.object._indices()]
                    rule_str = f'def {_name(component.name)}_(m_,{",".join(indices)}):\n    return {to_pyomo_str(component.object.value())}'
                else:
                    rule_str = f"def {_name(component.name)}_(m_):\n    return {to_pyomo_str(component.object.value())}"
                locals_ = {}
                exec(rule_str, {"pyo": pyo}, locals_)
                kwargs["initialize"] = locals_[f"{_name(component.name)}_"]

            if component.object.is_indexed():
                setattr(M, component.name, pyo.Param(*index_sets, **kwargs))
            else:
                setattr(M, component.name, pyo.Param(**kwargs))

        elif component.type == "variable":
            index_sets = [
                getattr(M, iset.name()) for iset in component.object._index_sets()
            ]
            indices = [i.name() for i in component.object._indices()]

            kwargs = {}
            if component.object.lower() or component.object.upper():
                if component.object.lower():
                    lower = f"{to_pyomo_str(component.object.lower())}"
                else:
                    lower = "None"
                if component.object.upper():
                    upper = f"{to_pyomo_str(component.object.upper())}"
                else:
                    upper = "None"
                if component.object.is_indexed():
                    rule_str = f'def {_name(component.name)}_bounds_(m_,{",".join(indices)}):\n    return {lower},{upper}'
                else:
                    rule_str = f"def {_name(component.name)}_bounds_(m_):\n    return {lower},{upper}"
                locals_ = {}
                exec(rule_str, {"pyo": pyo}, locals_)
                kwargs["bounds"] = locals_[f"{_name(component.name)}_bounds_"]

            if isinstance(
                component.object.value(), smoek.core.expr.nodes.NumberWrapper
            ):
                kwargs["initialize"] = component.object.value().value
            elif isinstance(
                component.object.value(), smoek.core.expr.nodes.DataWrapper
            ):
                kwargs["initialize"] = component.object.value().value
            elif component.object.value():
                if component.object.is_indexed():
                    rule_str = f'def {_name(component.name)}_(m_,{",".join(indices)}):\n    return {to_pyomo_str(component.object.value())}'
                else:
                    rule_str = f"def {_name(component.name)}_(m_):\n    return {to_pyomo_str(component.object.value())}"
                locals_ = {}
                exec(rule_str, {"pyo": pyo}, locals_)
                kwargs["initialize"] = locals_[f"{_name(component.name)}_"]
            kwargs["domain"] = domain[component.object.domain().id]

            if component.object.is_indexed():
                setattr(M, component.name, pyo.Var(*index_sets, **kwargs))
            else:
                setattr(M, component.name, pyo.Var(**kwargs))
                if component.object.fixed():
                    getattr(M, component.name).fix(
                        to_pyomo(component.object.value(), model=M)
                    )

        elif component.type == "expression":
            # TODO
            if component.object.is_indexed():
                pass
            else:
                pass

        elif component.type == "objective":
            if component.object.is_indexed():
                # TODO
                pass
            else:
                rule_str = f"def {_name(component.name)}_(m_):\n    return {to_pyomo_str(component.object.expr())}"
            locals_ = {}
            exec(rule_str, {"pyo": pyo}, locals_)
            setattr(
                M,
                component.name,
                pyo.Objective(rule=locals_[f"{_name(component.name)}_"]),
            )

        elif component.type == "constraint":
            index_sets = [
                getattr(M, iset.name()) for iset in component.object._index_sets()
            ]
            if component.object.is_indexed():
                indices = [i.name() for i in component.object._indices()]
                if len(index_sets) == 1:
                    rule_str = f"def {_name(component.name)}_(m_,{indices[0]}):\n    return {to_pyomo_str(component.object.expr())}"
                else:
                    rule_str = f'def {_name(component.name)}_(m_,{",".join(indices)}):\n    return {to_pyomo_str(component.object.expr())}'
            else:
                rule_str = f"def {_name(component.name)}_(m_):\n    return {to_pyomo_str(component.object.expr())}"
            locals_ = {}
            exec(rule_str, {"pyo": pyo}, locals_)
            setattr(
                M,
                component.name,
                pyo.Constraint(*index_sets, rule=locals_[f"{_name(component.name)}_"]),
            )

    return M
