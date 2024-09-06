import smoek.core.expr.nodes
import smoek.core.expr.functions
from smoek.core.utils import (
    BottomUpDepthFirstExpressionWalker,
    collect_info,
    valid_order,
)


class SmoekToNLPWalker(BottomUpDepthFirstExpressionWalker[str]):
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
                ret = f"std::pow({left}, {right})"
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

        elif isinstance(expr, smoek.core.expr.nodes.InequalityExprNode):
            right = self._stack.pop()
            body = self._stack.pop()
            left = self._stack.pop()
            ret = f"coek::inequality({left}, {body}, {right})"
            self._stack.append(ret)

        elif isinstance(expr, smoek.core.expr.functions.UnaryExprNode):
            if expr.operation == smoek.core.expr.nodes.ExpressionType.neg:
                arg = self._stack.pop()
                if isinstance(arg, smoek.core.expr.nodes.BinaryExprNode) and expr._left.operation in [
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


def to_cpp(expr, decl={}):
    return SmoekToNLPWalker().walk(expr, decl)


def generate_ipopt(*, model=None, data=None, outfile=None):
    """
    Generate a C++ code that defines functionst to evaluate a model along with first- and second-order derivatives.
    This writer is tailored to the API needed for IPOPT.

    If 'outfile' is None, then this is returned as a string.  Otherwise, 'outfile' is created with this code.
    """

    if data is None:
        data = {}
    components = []

    info = collect_info(model)
    order = valid_order(info)

    data_decls = []
    data_init = []
    eval_f = []
    eval_grad_f = []
    eval_grad_g = []
    eval_eval_jac_g = []
    eval_eval_h = []

    for name in order:
        component = info[name]
        coek_str = None

        if component.type == "index":
            pass

        elif component.type == "index_set":
            if isinstance(component.object, smoek.core.model.set_components.RangeSet):
                data_decls.append( f"std::vector<unsigned int> {component.name};" ) 
                data_init.append( f"unsigned int {component.name}_stop = {to_cpp(component.object._N)};" )
                data_init.append( f"for (size_t i=0; i<{component.name}_stop; i++) {component.name}.push_back(i);" )
            elif isinstance( component.object, smoek.core.model.set_components.SequenceSet ):
                data_decls.append( f"std::vector<unsigned int> {component.name};" ) 
                data_init.append( f"unsigned int {component.name}_stop = {to_cpp(component.object._stop)};" )
                data_init.append( f"for (size_t i=1; i<={component.name}_stop; i++) {component.name}.push_back(i);" )
            else:
                data_decls.append( f"std::vector<unsigned int> {component.name};" ) 
                coek_str = f"coek::ConcreteSet {component.name};"
                if component.name in data:
                    data_init.append( f'\nif (data.contains("{component.name}")) ' + '{\n' )
                    data_init.append( f'    data.get("{component.name}", {component.name});\n' )

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
                coek_str += f".value({to_cpp(component.object.value())})"
            coek_str += ';'
            if component.name in data:
                coek_str += f'\nif (data.contains("{component.name}")) ' + '{\n'
                coek_str += f'    {data[component.name]} {component.name}_value;\n'
                coek_str += f'    data.get("{component.name}", {component.name}_value);\n'
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
                    coek_str += f".lower({to_cpp(component.object.lower())})"
                if component.object.upper():
                    coek_str += f".upper({to_cpp(component.object.upper())})"
                if component.object.value():
                    coek_str += f".value({to_cpp(component.object.value())})"
                coek_str += ";"
            else:
                coek_str = f'auto {component.name} = coek::variable("{component.name}")'
                if component.object.lower():
                    coek_str += f".lower({to_cpp(component.object.lower())})"
                if component.object.upper():
                    coek_str += f".upper({to_cpp(component.object.upper())})"
                if component.object.value():
                    coek_str += f".value({to_cpp(component.object.value())})"
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
                coek_str = f'auto {component.name} = coek::objective("{component.name}").expr({to_cpp(component.object.expr())});'
            components.append(coek_str)
            components.append(f"model.add({component.name});")

        elif component.type == "constraint":
            if component.object.is_indexed():
                index_sets = [iset.name() for iset in component.object._index_sets()]
                indices = [i.name() for i in component.object._indices()]
                tmp = []
                for i,index_set in enumerate(index_sets):
                    index = indices[i]
                    tmp.append(f"Forall({index}).In({index_set})")
                coek_str = f'auto {component.name} = coek::constraint("{component.name}", {".".join(tmp)})'
                coek_str = coek_str + f".expr({to_cpp(component.object.expr())})"
                coek_str = coek_str + ";"
            else:
                coek_str = f'auto {component.name} = coek::constraint("{component.name}").expr({to_cpp(component.object.expr())});'

    code = f"""
#include <set>
#include <map>
#include <vector>
#include <coek/util/DataPortal.hpp>
#include "IpStdCInterfaceTypes.h"

namespace
{{
{"\n".join(data_decls)}

void initialize_model_data()
{{
{"\n".join(data_init)}
}}

void get_nlp_info(Index& n, Index& m, Index& nnz_jac_g, Index& nnz_h_lag, int& index_style)
{{
}}

Bool ipopt_capi_eval_f(Index n, Number* x, Bool new_x, Number* obj_value, UserDataPtr user_data)
{{
{"\n".join(eval_f)}
}}

Bool ipopt_capi_eval_grad_f(Index n, Number* x, Bool new_x, Number* grad_f, UserDataPtr user_data)
{{
{"\n".join(eval_grad_f)}
}}

Bool ipopt_capi_eval_g(Index n, Number* x, Bool new_x, Index m, Number* g, UserDataPtr user_data)
{{
{"\n".join(eval_grad_g)}
}}

Bool ipopt_capi_eval_jac_g(Index n, Number* x, Bool new_x, Index m, Index nele_jac, Index* iRow,
                           Index* jCol, Number* values, UserDataPtr user_data)
{{
{"\n".join(eval_eval_jac_g)}
}}

Bool ipopt_capi_eval_h(Index n, Number* x, Bool new_x, Number obj_factor, Index m, Number* lambda,
                       Bool new_lambda, Index nele_hess, Index* iRow, Index* jCol, Number* values,
                       UserDataPtr user_data)
{{
{"\n".join(eval_eval_h)}
}}

Bool ipopt_capi_intermediate_cb(Index /*alg_mod*/, Index iter_count, Number /*obj_value*/,
                                Number /*inf_pr*/, Number /*inf_du*/, Number /*mu*/,
                                Number /*d_norm*/, Number /*regularization_size*/,
                                Number /*alpha_du*/, Number /*alpha_pr*/, Index /*ls_trials*/,
                                UserDataPtr user_data)
{{
return TRUE;
}}

}}

IpoptProblem generate_{model.name}(const coek::DataPortal& data, CreateIpoptProblem_func_t func_ptr, std::vector<Number>& last_x,  std::vector<Number>& last_g)
{{
}}
"""

    if outfile is None:
        return code
    else:                                                           # pragma: nocover
        with open(outfile, "w") as OUTPUT:
            OUTPUT.write(code)


def generate(*, model=None, data=None, outfile=None, nlp="ipopt"):
    """
    Generate a C++ code that defines functionst to evaluate a model along with first- and second-order derivatives.
    This writer is tailored to the API needed for IPOPT, but the intention is to make this suitable for other NLP solver
    interfaces.

    If 'outfile' is None, then this is returned as a string.  Otherwise, 'outfile' is created with this code.
    """

    if nlp == "ipopt":
        return generate_ipopt(model=model, data=data, outfile=outfile)
    raise RuntimeError("Unknown NLP interface: "+nlp)
