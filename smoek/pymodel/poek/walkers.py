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
    import poek as pk
    poek_available = True
except:         # pragma: nocover
    poek_available = False

if poek_available:
    domain = {
        Reals.id: pk.VariableTypes.Reals,
        Integers.id: pk.VariableTypes.Integers,
        Binary.id: pk.VariableTypes.Binary,
        }
    unary = {
        "sin": pk.sin,
        "cos": pk.cos,
        "tan": pk.tan,
        "asin": pk.asin,
        "acos": pk.acos,
        "atan": pk.atan,
        "log": pk.log,
        "log10": pk.log10,
        }


class SmoekToPoekExprWalker(BottomUpDepthFirstExpressionWalker[str]):
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
                ret = left ** right
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
            ret = pk.inequality(left, body, right)
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            if expr.operation == "neg":
                ret = self._stack.pop()
                self._stack.append(- ret)
            else:
                arg = self._stack.pop()
                ret = unary[expr.operation](arg)
                self._stack.append(ret)

        elif isinstance(expr, smoek.core.model.var_components.ScalarVariable):
            self._stack.append( getattr(self._model, expr.name()) )

        elif isinstance(expr, smoek.core.model.data_components.Parameter):
            self._stack.append( getattr(self._model, expr.name()) )

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


class SmoekToPoekStringWalker(BottomUpDepthFirstExpressionWalker[str]):
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
            elif expr.operation in [ExpressionType.eq, ExpressionType.leq, ExpressionType.geq]:
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
            ret = f"pk.inequality({left}, {body}, {right})"
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            if expr.operation == "neg":
                arg = self._stack.pop()
                if isinstance(expr._arg, smoek.core.expr.nodes.BinaryExprNode) and expr._arg.operation in [
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
                ret = f"pk.{expr.operation}({arg})"
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
def to_poek(expr, decl={}, model=None):
    return SmoekToPoekExprWalker().walk(expr, decl, model)

def to_poek_str(expr, decl={}):
    return SmoekToPoekStringWalker().walk(expr, decl, "m")


class Tmp(object): pass

def generate(*, model=None, data=None):
    """
    Generate a Poek model described by smoek.
    """
    if not poek_available:     # pragma: nocover
        return None

    if data is None:
        data = {}

    info = collect_info(model)
    order = valid_order(info)

    M = Tmp()
    M._model = pk.model()

    for name in order:
        component = info[name]
        poek_str = None

        if component.type == "index":
            continue

        elif component.type == "index_set":
            if isinstance(component.object, smoek.core.model.set_components.RangeSet):
                setattr(M, component.name, pk.RangeSet(0, to_poek(component.object._N, model=M)))
            elif isinstance(component.object, smoek.core.model.set_components.SequenceSet):
                setattr(M, component.name, pk.RangeSet(to_poek(component.object._start, model=M), to_poek(component.object._stop, model=M)))
            else:
                def set_(m):
                    return data[component.name]
                setattr(M, component.name, pk.Set(initialize=set_))

        elif component.type == "parameter" or component.type == "data":
            index_sets = [ getattr(M, iset.name()) for iset in component.object._index_sets() ]
            indices = [i.name() for i in component.object._indices()]

            args = []
            kwargs = {}

            # name
            if component.object.name():
                args.append( component.object.name() )

            # value
            if component.name in data:
                kwargs['value']= data[component.name]
            elif isinstance(component.object.value(), smoek.core.expr.nodes.NumberWrapper):
                kwargs['value']= component.object.value().value
            elif component.object.value():
                if component.object.is_indexed():
                    rule_str = f'{component.name}_ = {to_poek_str(component.object.value())}'
                else:
                    rule_str = f'{component.name}_ = {to_poek_str(component.object.value())}'
                locals_ = {}
                exec(rule_str, {"pk":pk}, locals_)
                kwargs['value']= locals_[f"{component.name}_"]

            param = pk.parameter(*args, **kwargs)
            setattr(M, component.name, param)

        elif component.type == "variable":
            index_sets = [ getattr(M, iset.name()) for iset in component.object._index_sets() ]
            indices = [i.name() for i in component.object._indices()]

            kwargs={}
            # name
            if component.object.name():
                kwargs['name']= component.object.name()

            # lb or ub
            if component.object.lower() or component.object.upper():
                if component.object.lower():
                    lower = f'{to_poek_str(component.object.lower())}'
                else:
                    lower = "None"
                if component.object.upper():
                    upper = f'{to_poek_str(component.object.upper())}'
                else:
                    upper = "None"
                locals_ = {}
                exec(f"{component.name}_lower_ = {lower}", {"pk":pk}, locals_)
                exec(f"{component.name}_upper_ = {upper}", {"pk":pk}, locals_)
                kwargs['lb'] = locals_[f"{component.name}_lower_"]
                kwargs['ub'] = locals_[f"{component.name}_upper_"]

            # value
            if isinstance(component.object.value(), smoek.core.expr.nodes.NumberWrapper):
                kwargs['value']= component.object.value().value
            elif component.object.value():
                if component.object.is_indexed():
                    rule_str = f'{component.name}_ = {to_poek_str(component.object.value())}'
                else:
                    rule_str = f'{component.name}_ = {to_poek_str(component.object.value())}'
                locals_ = {}
                exec(rule_str, {"pk":pk}, locals_)
                kwargs['value'] = locals_[f"{component.name}_"]

            # binary or integer
            if component.object.domain().id == Integers.id:
                kwargs['integer'] = true
            elif component.object.domain().id == Binary.id:
                kwargs['binary'] = true

            # fixed
            if component.object.fixed():
                kwargs['fixed'] = component.object.fixed()

            if component.object.is_indexed():
                var = M._model.add_variable(*index_sets, **kwargs)
            else:
                var = M._model.add_variable(**kwargs)
            setattr(M, component.name, var)

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
                rule_str = f'def {component.name}_(m):\n    return {to_poek_str(component.object.expr())}'
            locals_ = {}
            exec(rule_str, {"pk":pk}, locals_)
            M._model.add_objective( locals_[f"{component.  name}_"](M) )

        elif component.type == "constraint":
            index_sets = [ getattr(M, iset.name()) for iset in component.object._index_sets() ]
            if component.object.is_indexed():
                indices = [i.name() for i in component.object._indices()]
                if len(index_sets) == 1:
                    rule_str = f'def {component.name}_(m,{indices[0]}):\n    return {to_poek_str(component.object.expr())}'
                else:
                    rule_str = f'def {component.name}_(m,{",".join(indices)}):\n    return {to_poek_str(component.object.expr())}'
            else:
                rule_str = f'def {component.name}_(m):\n    return {to_poek_str(component.object.expr())}'
            locals_ = {}
            exec(rule_str, {"pk":pk}, locals_)
            M._model.add_constraint( locals_[f"{component.name}_"](M) )

    return M._model

