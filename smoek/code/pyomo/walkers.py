import smoek.core.expr.nodes
from smoek.core.expr.nodes import ExpressionType
import smoek.core.expr.functions
from smoek.core.utils import (
    BottomUpDepthFirstExpressionWalker,
    collect_info,
    valid_order,
)


class SmoekToPyomoWalker(BottomUpDepthFirstExpressionWalker[str]):
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
            if expr.operation == "pow":
                ret = f"pow({left}, {right})"
            elif expr.operation in ["==", "<=", ">="]:
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
            arg = self._stack.pop()
            ret = f"pyo.{expr.operation}({arg})"
            self._stack.append(ret)

        # elif isinstance(expr, smoek.core.model.var_components.ScalarVariable):
        #    self._stack.append( expr.name() )

        # elif isinstance(expr, smoek.core.model.data_components.Parameter):
        #    self._stack.append( expr.name() )

        # elif isinstance(expr, smoek.core.model.data_components.Data):
        #    self._stack.append( expr.name() )

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

        # elif isinstance(expr, smoek.core.expr.functions.ProdExprNode):
        #    body = self._stack.pop()
        #    ret = f"prod({expr._forall.to_string()}, {body})"
        #    self._stack.append(ret)

        # elif isinstance(expr, smoek.core.expressions.Expression):
        #    body = self._stack.pop()
        #    ret = f"({body})"
        #    self._stack.append(ret)

        else:  # pragma: nocover
            raise NotImplementedError(
                f"Expression node {expr} of type {type(expr)} not supported in ExpressionToStringWalker"
            )


def to_pyomo(expr, decl={}, model="M"):
    return SmoekToPyomoWalker().walk(expr, decl, model)


def generate(*, model=None, data=None, outfile=None):
    """
    Generate a C++ code that generates a Coek model described by smoek.

    If 'outfile' is None, then this is returned as a string.  Otherwise, 'outfile' is created with this code.
    """

    if data is None:
        data = {}
    components = []

    info = collect_info(model)
    order = valid_order(info)

    for name in order:
        component = info[name]
        pyomo_str = None

        if component.type == "index":
            # pyomo_str = f'auto {component.name} = coek::set_element("{component.name}");'
            # components.append(pyomo_str)
            continue

        elif component.type == "index_set":
            if isinstance(component.object, smoek.core.model.set_components.RangeSet):
                pyomo_str = f"    M.{component.name} = pyo.RangeSet(0, {to_pyomo(component.object._N)})"
            elif isinstance(
                component.object, smoek.core.model.set_components.SequenceSet
            ):
                pyomo_str = f"    M.{component.name} = pyo.RangeSet({to_pyomo(component.object._start)}, {to_pyomo(component.object._stop)}+1)"
            else:
                pyomo_str = f'    M.{component.name} = pyo.Set(initialize=data["{component.name}"])'
            components.append(pyomo_str)

        elif component.type == "parameter" or component.type == "data":
            mutable = component.type == "parameter"
            if component.name in data:
                initial_value = f', initialize=data["{component.name}"]'
                # if component.object.value():
                #    initial_value = f', initialize=data["{component.name}"]'
                # else:
                #    initial_value = f', initialize={component.object.value()}'
            elif component.object.value():
                initial_value = f", initialize={to_pyomo(component.object.value())}"
            else:
                initial_value = ""

            if component.object.is_indexed():
                index_sets = [
                    "M." + iset.name() for iset in component.object._index_sets()
                ]
                if len(index_sets) == 1:
                    pyomo_str = f"    M.{component.name} = pyo.Param({index_sets[0]}, mutable={mutable}{initial_value})"
                else:
                    pyomo_str = f'    M.{component.name} = pyo.Param({", ".join(index_sets)}, mutable={mutable}{initial_value})'
            else:
                pyomo_str = f"    M.{component.name} = pyo.Param(mutable={mutable}{initial_value})"
            components.append(pyomo_str)

        elif component.type == "variable":
            varargs = []
            if component.object.lower() or component.object.upper():
                if component.object.lower():
                    lower = to_pyomo(component.object.lower())
                else:
                    lower = "None"
                if component.object.upper():
                    upper = to_pyomo(component.object.upper())
                else:
                    upper = "None"
                varargs.append(f"bounds=({lower},{upper})")
            if component.object.value():
                varargs.append(f"initialize={to_pyomo(component.object.value())}")

            if component.object.is_indexed():
                index_sets = [
                    "M." + iset.name() for iset in component.object._index_sets()
                ]
                if len(varargs) > 0:
                    varargs = ", " + ", ".join(varargs)
                else:
                    varargs = ""
                if len(index_sets) == 1:
                    pyomo_str = (
                        f"    M.{component.name} = pyo.Var({index_sets[0]}{varargs})"
                    )
                else:
                    pyomo_str = f'    M.{component.name} = pyo.Var({", ".join(index_sets)}{varargs})'
            else:
                varargs = ", ".join(varargs)
                pyomo_str = f"    M.{component.name} = pyo.Var({varargs})"
                if component.object.fixed():
                    pyomo_str = pyomo_str + f"\n    M.{component.name}.fix()"
            components.append(pyomo_str)

        elif component.type == "expression":
            if component.object.is_indexed():
                # setattr(M, component.name, pyo.Expression(initialize=component.object.data()), mutable=False)
                pass
            else:
                # setattr(M, component.name, pyo.Expression(expr=to_pyomo(component.object.expr()), mutable=False))
                pass
            components.append(pyomo_str)

        elif component.type == "objective":
            if component.object.is_indexed():
                # setattr(M, component.name, pyo.Expression(initialize=component.object.data()), mutable=False)
                pass
            else:
                pyomo_str = f"    M.{component.name} = pyo.Objective(expr={to_pyomo(component.object.expr())})"
            components.append(pyomo_str)

        elif component.type == "constraint":
            if component.object.is_indexed():
                index_sets = [
                    "M." + iset.name() for iset in component.object._index_sets()
                ]
                indices = [i.name() for i in component.object._indices()]
                conargs = ""
                if len(index_sets) == 1:
                    pyomo_str = f'    def {component.name}_(m,{indices[0]}):\n        return {to_pyomo(component.object.expr(), model="m")}\n'
                    pyomo_str = (
                        pyomo_str
                        + f"    M.{component.name} = pyo.Constraint({index_sets[0]}{conargs}, rule={component.name}_)"
                    )
                else:
                    pyomo_str = f'    def {component.name}_(m,{",".join(indices)}):\n        return {to_pyomo(component.object.expr(), model="m")}\n'
                    pyomo_str = (
                        pyomo_str
                        + f'    M.{component.name} = pyo.Constraint({", ".join(index_sets)}{conargs}, rule={component.name}_)'
                    )
            else:
                pyomo_str = f"    M.{component.name} = pyo.Constraint(expr={to_pyomo(component.object.expr())})"
            components.append(pyomo_str)

        if pyomo_str is None or components[-1] is None:  # pragma: nocover
            print("ERROR", component.name, component.type)
        if pyomo_str is not None:
            components.append("")

    add_components = "\n".join(components)
    code = f"""
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_{model.name}(data):
    M = pyo.ConcreteModel("{model.name}")

{add_components}
    return M
"""

    if outfile is None:
        return code
    else:  # pragma: nocover
        with open(outfile, "w") as OUTPUT:
            OUTPUT.write(code)
