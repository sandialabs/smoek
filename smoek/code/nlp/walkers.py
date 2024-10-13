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
                ret = f"pow({left}, {right})"
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
                if isinstance(
                    arg, smoek.core.expr.nodes.BinaryExprNode
                ) and expr._left.operation in [
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
                ret = f"std::{expr.operation}({arg})"
                self._stack.append(ret)

        # elif isinstance(expr, smoek.core.model.var_components.ScalarVariable):
        #    self._stack.append( expr.name() )

        # elif isinstance(expr, smoek.core.model.data_components.Parameter):
        #    self._stack.append( expr.name() )

        # elif isinstance(expr, smoek.core.model.data_components.Data):
        #    self._stack.append( expr.name() )

        elif isinstance(expr, smoek.core.expr.nodes.ComponentIndicesNode):
            indices = [str(index) for index in expr._indices]
            if len(indices) == 1:
                ret = f"{expr._component.name()}[{indices[0]}]"
            else:
                ret = f'{expr._component.name()}[{{{", ".join(indices)}}}]'
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

        else:  # pragma: nocover
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
    copy_into_vars = []

    for name in order:
        component = info[name]

        if component.type == "index":
            pass

        elif component.type == "index_set":
            if isinstance(component.object, smoek.core.model.set_components.RangeSet):
                data_decls.append(f"std::vector<int> {component.name};")
                data_init.append(
                    f"int {component.name}_stop = {to_cpp(component.object._N)};"
                )
                data_init.append(
                    f"for (int i=0; i<{component.name}_stop; i++) {component.name}.push_back(i);"
                )
            elif isinstance(
                component.object, smoek.core.model.set_components.SequenceSet
            ):
                data_decls.append(f"std::vector<int> {component.name};")
                data_init.append(
                    f"int {component.name}_stop = {to_cpp(component.object._stop)};"
                )
                data_init.append(
                    f"for (int i=1; i<={component.name}_stop; i++) {component.name}.push_back(i);"
                )
            else:
                data_decls.append(f"std::vector<int int> {component.name};")
                if component.name in data:
                    data_init.append(f'if (data.contains("{component.name}")) ')
                    data_init.append(
                        f'    data.get("{component.name}", {component.name});'
                    )

        elif component.type == "parameter":
            if component.object.is_indexed():
                index_sets = [iset.name() for iset in component.object._index_sets()]
                if len(index_sets) == 1:
                    data_decls.append(f"std::map<int,double> {component.name};")
                else:
                    data_decls.append(
                        f'std::map<std::tuple<{",".join(["int"]*len(index_sets))}>,double> {component.name};'
                    )
                # TODO: Do we provide a dense initial value for keys specified for a parameter?  C++ doesn't have a map with default values.
            else:
                data_decls.append(f"double {component.name};")
                if component.object.value():
                    data_init.append(
                        f"{component.name} = {to_cpp(component.object.value())};"
                    )
            if component.name in data:
                data_init.append(f'if (data.contains("{component.name}")) ')
                data_init.append(
                    f'    data.get("{component.name}", {component.name});\n'
                )

        elif component.type == "data":
            if component.object.is_indexed():
                pass
            else:
                pass

        elif component.type == "variable":
            if component.object.is_indexed():
                index_sets = [iset.name() for iset in component.object._index_sets()]
                if len(index_sets) == 1:
                    data_decls.append(f"std::map<int,double> {component.name};")
                else:
                    data_decls.append(
                        f'std::map<std::tuple<{",".join(["int"]*len(index_sets))}>,double> {component.name};'
                    )
                # data_decls.append( f'std::vector<Number> {component.name}_lower;' )
                # data_decls.append( f'std::vector<Number> {component.name}_upper;' )
                # data_decls.append( f'std::vector<Number> {component.name}_init;' )

                prefix = ""
                for isp in component.object._index_set_pairs():
                    data_init.append(
                        prefix + f"for (auto& {isp.index.name()}: {isp.set.name()})"
                    )
                    prefix += "  "
                data_init.append(prefix + "{")
                if len(component.object._index_set_pairs()) == 1:
                    data_init.append(
                        prefix
                        + f'{component.name}[{",".join(isp.index.name() for isp in component.object._index_set_pairs())}] = 0;'
                    )
                else:
                    data_init.append(
                        prefix
                        + f'{component.name}[{{{",".join(isp.index.name() for isp in component.object._index_set_pairs())}}}] = 0;'
                    )
                if component.object.lower():
                    data_init.append(
                        prefix + f"x_lower_[i_] = {to_cpp(component.object.lower())};"
                    )
                else:
                    data_init.append(prefix + f"x_lower_[i_] = -INFTY;")
                if component.object.upper():
                    data_init.append(
                        prefix + f"x_upper_[i_] = {to_cpp(component.object.upper())};"
                    )
                else:
                    data_init.append(prefix + f"x_upper_[i_] = -INFTY;")
                if component.object.value():
                    data_init.append(
                        prefix + f"x_init_[i_] = {to_cpp(component.object.value())};"
                    )
                else:
                    data_init.append(prefix + f"x_init_[i_] = 0.0;")
                data_init.append(prefix + "i_++;")
                data_init.append(prefix + "}")
                data_init.append(f"nv += {component.name}.size();")

                prefix = ""
                for isp in component.object._index_set_pairs():
                    copy_into_vars.append(
                        prefix + f"for (auto& {isp.index.name()}: {isp.set.name()})"
                    )
                    prefix += "  "
                if len(component.object._index_set_pairs()) == 1:
                    copy_into_vars.append(
                        prefix
                        + f'{component.name}[{",".join(isp.index.name() for isp in component.object._index_set_pairs())}] = x_[i_++];'
                    )
                else:
                    copy_into_vars.append(
                        prefix
                        + f'{component.name}[{{{",".join(isp.index.name() for isp in component.object._index_set_pairs())}}}] = x_[i_++];'
                    )
            else:
                data_decls.append(f"double {component.name};")
                # data_decls.append( f'double {component.name}_lower;' )
                # data_decls.append( f'double {component.name}_upper;' )
                # data_decls.append( f'double {component.name}_init;' )

                data_init.append(f"nv++; //{component.name}")
                if component.object.lower():
                    data_init.append(
                        f"x_lower_[i_++] = {to_cpp(component.object.lower())};"
                    )
                else:
                    data_init.append(f"x_lower_[i_++] = -INFTY;")
                if component.object.upper():
                    data_init.append(
                        f"x_upper_[i_++] = {to_cpp(component.object.upper())};"
                    )
                else:
                    data_init.append(f"x_upper_[i_++] = INFTY;")
                if component.object.value():
                    data_init.append(
                        f"x_init_[i_++] = {to_cpp(component.object.value())};"
                    )
                else:
                    data_init.append(f"x_init_[i_++] = 0.0;")

                copy_into_vars.append(f"{component.name} = x_[i_++];")

        elif component.type == "expression":
            if component.object.is_indexed():
                pass
            else:
                pass

        elif component.type == "objective":
            if component.object.is_indexed():
                # setattr(M, component.name, pyo.Expression(initialize=component.object.data()), mutable=False)
                pass
            else:
                if component.object.sense():
                    data_decls.append(f"const Number objsense = 1.0;")
                else:
                    data_decls.append(f"const Number objsense = -1.0;")
                eval_f.append(
                    f"*obj_value_ = objsense * ({to_cpp(component.object.expr())});"
                )

        elif component.type == "constraint":
            if component.object.is_indexed():
                index_sets = [iset.name() for iset in component.object._index_sets()]
                indices = [i.name() for i in component.object._indices()]
                tmp = []
                for i, index_set in enumerate(index_sets):
                    index = indices[i]
                    tmp.append(f"Forall({index}).In({index_set})")
                coek_str = f'auto {component.name} = coek::constraint("{component.name}", {".".join(tmp)})'
                coek_str = coek_str + f".expr({to_cpp(component.object.expr())})"
                coek_str = coek_str + ";"
            else:
                coek_str = f'auto {component.name} = coek::constraint("{component.name}").expr({to_cpp(component.object.expr())});'

    code = f"""
#include <cassert>
#include <set>
#include <map>
#include <vector>
#include <cmath>
#include <coek/util/DataPortal.hpp>
#include "IpStdCInterfaceTypes.h"

#define INFTY 1e100

namespace
{{
size_t nv;
size_t nc;
std::vector<Number> x_lower_;
std::vector<Number> x_upper_;
std::vector<Number> x_init_;
std::vector<Number> c_lower_;
std::vector<Number> c_upper_;
{"\n".join(data_decls)}

void initialize_model_data(const coek::DataPortal& data)
{{
size_t i_=0;
nv=0;
nc=0;
{"\n".join(data_init)}
}}

void get_nlp_info(Index& n, Index& m, Index& nnz_jac_g, Index& nnz_h_lag, int& index_style)
{{
n = nv;
m = nc;
nnz_jac_g = 0;
nnz_h_lag = 0;
index_style = 0;
}}

void get_bounds_info(Index n, Number* x_L, Number* x_U, Index m, Number* c_L, Number* c_U)
{{
assert(nv == n);
for (size_t i=0; i<nv; i++) {{
    x_L[i] = x_lower_[i];
    x_U[i] = x_upper_[i];
    }}
assert(nc == m);
for (size_t i=0; i<nc; i++) {{
    c_L[i] = c_lower_[i];
    c_U[i] = c_upper_[i];
    }}
}}

void copy_into_vars(Index n_, Number* x_)
{{
size_t i_=0;
{"\n".join(copy_into_vars)}
assert(i_ == n_);
}}

Number* array_ptr(std::vector<Number>& v)
{{
    if (v.size() == 0)
        return 0;
    return &(v[0]);
}}

Bool ipopt_capi_eval_f(Index n_, Number* x_, Bool new_x_, Number* obj_value_, UserDataPtr /*user_data*/)
{{
if (new_x_)
    copy_into_vars(n_, x_);
{"\n".join(eval_f)}
}}

Bool ipopt_capi_eval_grad_f(Index n_, Number* x_, Bool new_x_, Number* grad_f_, UserDataPtr /*user_data*/)
{{
{"\n".join(eval_grad_f)}
}}

Bool ipopt_capi_eval_g(Index n_, Number* x_, Bool new_x_, Index m_, Number* g_, UserDataPtr /*user_data*/)
{{
{"\n".join(eval_grad_g)}
}}

Bool ipopt_capi_eval_jac_g(Index n_, Number* x_, Bool new_x_, Index m_, Index nele_jac_, Index* iRow_,
                           Index* jCol_, Number* values_, UserDataPtr /*user_data*/)
{{
{"\n".join(eval_eval_jac_g)}
}}

Bool ipopt_capi_eval_h(Index n_, Number* x_, Bool new_x_, Number obj_factor_, Index m_, Number* lambda_,
                       Bool new_lambda_, Index nele_hess_, Index* iRow_, Index* jCol_, Number* values_,
                       UserDataPtr /*user_data*/)
{{
{"\n".join(eval_eval_h)}
}}

Bool ipopt_capi_intermediate_cb(Index /*alg_mod*/, Index /*iter_count*/, Number /*obj_value*/,
                                Number /*inf_pr*/, Number /*inf_du*/, Number /*mu*/,
                                Number /*d_norm*/, Number /*regularization_size*/,
                                Number /*alpha_du*/, Number /*alpha_pr*/, Index /*ls_trials*/,
                                UserDataPtr /*user_data*/)
{{
return TRUE;
}}

}}

IpoptProblem generate_{model.name}(const coek::DataPortal& data, CreateIpoptProblem_func_t func_ptr, std::vector<Number>& last_x,  std::vector<Number>& last_g)
{{
    initialize_model_data(data);

    Index n;
    Index m;
    Index nnz_jac_g;
    Index nnz_h_lag;
    int index_style;
    get_nlp_info(n, m, nnz_jac_g, nnz_h_lag, index_style);
    size_t n_ = static_cast<size_t>(n);
    size_t m_ = static_cast<size_t>(m);

    last_x.resize(n_);
    for (size_t i=0; i<n_; i++)
        last_x[i] = x_init_[i];
    last_g.resize(m_);
    // TODO - Defaults to zero?

    std::vector<Number> x_L(n_);
    std::vector<Number> x_U(n_);
    std::vector<Number> g_L(m_);
    std::vector<Number> g_U(m_);
    get_bounds_info(n, array_ptr(x_L), array_ptr(x_U), m, array_ptr(g_L), array_ptr(g_U));

return (*func_ptr)(
        n, array_ptr(x_L), array_ptr(x_U), m, array_ptr(g_L), array_ptr(g_U), nnz_jac_g, nnz_h_lag,
        index_style, &ipopt_capi_eval_f, &ipopt_capi_eval_g, &ipopt_capi_eval_grad_f,
        &ipopt_capi_eval_jac_g, &ipopt_capi_eval_h);
}}
"""

    if outfile is None:
        return code
    else:  # pragma: nocover
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
    raise RuntimeError("Unknown NLP interface: " + nlp)
