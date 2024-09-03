import smoek.core.expr.nodes
import smoek.core.expr.functions
from smoek.core.utils import (
    BottomUpDepthFirstExpressionWalker,
    collect_info,
    valid_order,
)


class SmoekToCoekWalker(BottomUpDepthFirstExpressionWalker[str]):
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
            if expr.operation == "pow":
                ret = f"coek::pow({left}, {right})"
            elif expr.operation in ["==", "<=", ">="]:
                ret = f"{left} {expr.operation} {right}"
            else:
                if isinstance(
                    expr._right, smoek.core.expr.nodes.BinaryExprNode
                ) and expr._right.operation in ["+", "-", "*", "/"]:
                    right = f"({right})"
                if isinstance(
                    expr._left, smoek.core.expr.nodes.BinaryExprNode
                ) and expr._left.operation in ["+", "-", "*", "/"]:
                    left = f"({left})"
                ret = f"{left} {expr.operation} {right}"
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            arg = self._stack.pop()
            ret = f"coek::{expr.operation}({arg})"
            self._stack.append(ret)

        # elif isinstance(expr, smoek.core.model.var_components.ScalarVariable):
        #    self._stack.append( expr.name() )

        # elif isinstance(expr, smoek.core.model.data_components.Parameter):
        #    self._stack.append( expr.name() )

        # elif isinstance(expr, smoek.core.model.data_components.Data):
        #    self._stack.append( expr.name() )

        elif isinstance(expr, smoek.core.expr.nodes.ComponentIndicesNode):
            indices = [str(index) for index in expr._indices]
            ret = f'{expr._component.name()}({", ".join(indices)})'
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.nodes.ExprLeaf):
            ret = f"{expr.to_string()}"
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.functions.SumExprNode):
            body = self._stack.pop()
            forall = []
            for pair in expr._forall._index_set_pairs:
                index = str(pair.index)
                index_set = pair.set.name()
                forall.append(f"coek::Forall({index}).In({index_set})")
            ret = f"coek::Sum({body}, {'.'.join(forall)})"
            self._stack.append(ret)

        # elif isinstance(expr, smoek.core.expr.functions.ProdExprNode):
        #    body = self._stack.pop()
        #    ret = f"prod({expr._forall.to_string()}, {body})"
        #    self._stack.append(ret)

        # elif isinstance(expr, smoek.core.expressions.Expression):
        #    body = self._stack.pop()
        #    ret = f"({body})"
        #    self._stack.append(ret)

        else:                                   # pragma: nocover
            raise NotImplementedError(
                f"Expression node {expr} of type {type(expr)} not supported in ExpressionToStringWalker"
            )


def to_coek(expr, decl={}):
    return SmoekToCoekWalker().walk(expr, decl)


def generate(*, model=None, data=None, outfile=None, compact=True):
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
        coek_str = None

        if component.type == "index":
            coek_str = f'auto {component.name} = coek::set_element("{component.name}");'
            components.append(coek_str)

        elif component.type == "index_set":
            if isinstance(component.object, smoek.core.model.set_components.RangeSet):
                coek_str = f"auto {component.name} = coek::RangeSet(0, {to_coek(component.object._N)});"
            elif isinstance(
                component.object, smoek.core.model.set_components.SequenceSet
            ):
                coek_str = f"auto {component.name} = coek::RangeSet({to_coek(component.object._start)}, {to_coek(component.object._stop)}+1);"
            else:
                coek_str = f"auto {component.name} = coek::Set();"
                if component.name in data:
                    coek_str += f'\nif (data.contains("{component.name}") ' + '{\n'
                    coek_str += f'    {data[component.name]} {component.name}_value;\n'
                    coek_str += f'    data.get<{data[component.name]}>("{component.name}", {component.name}_value);\n'
                    coek_str += f'    {component.name}.value({component.name}_value);\n' + '}'
            components.append(coek_str)

        elif component.type == "parameter":
            if component.object.is_indexed():
                index_sets = [iset.name() for iset in component.object._index_sets()]
                if len(index_sets) == 1:
                    coek_str = f'auto {component.name} = coek::parameter("{component.name}", {index_sets[0]})'
                else:
                    coek_str = f'auto {component.name} = coek::parameter("{component.name}", {"*".join(index_sets)})'
            else:
                coek_str = (
                    f'auto {component.name} = coek::parameter("{component.name}")'
                )
            if component.object.value():
                coek_str += f".value({to_coek(component.object.value())})"
            coek_str += ';'
            if component.name in data:
                coek_str += f'\nif (data.contains("{component.name}") ' + '{\n'
                coek_str += f'    {data[component.name]} {component.name}_value;\n'
                coek_str += f'    data.get<{data[component.name]}>("{component.name}", {component.name}_value);\n'
                coek_str += f'    {component.name}.value({component.name}_value);\n' + '}'
            components.append(coek_str)

        elif component.type == "data":
            if component.object.is_indexed():
                pass
            else:
                pass
            components.append(coek_str)

        elif component.type == "variable":
            if component.object.is_indexed():
                index_sets = [iset.name() for iset in component.object._index_sets()]
                if len(index_sets) == 1:
                    coek_str = f'auto {component.name} = coek::variable("{component.name}", {index_sets[0]})'
                else:
                    coek_str = f'auto {component.name} = coek::variable("{component.name}", {"*".join(index_sets)})'
                if component.object.lower():
                    coek_str += f".lower({to_coek(component.object.lower())})"
                if component.object.upper():
                    coek_str += f".upper({to_coek(component.object.upper())})"
                if component.object.value():
                    coek_str += f".value({to_coek(component.object.value())})"
                coek_str += ";"
            else:
                coek_str = f'auto {component.name} = coek::variable("{component.name}")'
                if component.object.lower():
                    coek_str += f".lower({to_coek(component.object.lower())})"
                if component.object.upper():
                    coek_str += f".upper({to_coek(component.object.upper())})"
                if component.object.value():
                    coek_str += f".value({to_coek(component.object.value())})"
                coek_str += ";"
            components.append(coek_str)
            components.append(f"model.add({component.name});")

        elif component.type == "expression":
            if component.object.is_indexed():
                # setattr(M, component.name, pyo.Expression(initialize=component.object.data()), mutable=False)
                pass
            else:
                # setattr(M, component.name, pyo.Expression(expr=to_pyomo(component.object.expr()), mutable=False))
                pass
            components.append(coek_str)
            components.append(f"model.add({component.name});")

        elif component.type == "objective":
            if component.object.is_indexed():
                # setattr(M, component.name, pyo.Expression(initialize=component.object.data()), mutable=False)
                pass
            else:
                coek_str = f'auto {component.name} = coek::objective("{component.name}").expr({to_coek(component.object.expr())});'
            components.append(coek_str)
            components.append(f"model.add({component.name});")

        elif component.type == "constraint":
            if component.object.is_indexed():
                index_sets = [iset.name() for iset in component.object._index_sets()]
                indices = [i.name() for i in component.object._indices()]
                if len(index_sets) == 1:
                    coek_str = f'auto {component.name} = coek::constraint("{component.name}", {index_sets[0]})'
                else:
                    coek_str = f'auto {component.name} = coek::constraint("{component.name}", {"*".join(index_sets)})'
                if compact:
                    coek_str = coek_str + f".expr({to_coek(component.object.expr())})"
                    for i,index_set in enumerate(index_sets):
                        index = indices[i]
                        coek_str = coek_str + f".Forall({index}).In({index_set})"
                    coek_str = coek_str + ";"
            else:
                coek_str = f'auto {component.name} = coek::constraint("{component.name}").expr({to_coek(component.object.expr())});'
            components.append(coek_str)
            components.append(f"model.add({component.name});")

        if coek_str is None or components[-1] is None:              # pragma: nocover
            print("ERROR", component.name, component.type)
        if coek_str is not None:
            components.append("")

    add_components = "\n".join(components)
    code = f"""
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::Model generate_{model.name}(coek::DataPortal& data)
\u007b
coek::Model model;
model.name("{model.name}");

{add_components}
return model;
\u007d
"""

    if outfile is None:
        return code
    else:                                                           # pragma: nocover
        with open(outfile, "w") as OUTPUT:
            OUTPUT.write(code)
