import os

# import sympy as sp

# from jinja2 import Environment, FileSystemLoader

# TODO: remove the reliance on types
from smoek.core.expr.nodes import (
    ExprLeaf,
    BinaryExprNode,
    ComponentIndicesNode,
    UnaryExprNode,
    ExpressionType,
)
from smoek.core.expr.functions import SumExprNode, ProdExprNode
from smoek.core.model.expressions import Expression, Objective
from smoek.core.model.model_components import Model
from smoek.core.model.var_components import (
    ScalarVariable,
    IndexedVariable,
    Reals,
    Binary,
)
from smoek.core.utils import BottomUpDepthFirstExpressionWalker


class ExpressionToLatexStringWalker(BottomUpDepthFirstExpressionWalker[str]):
    def __init__(self):
        super().__init__()
        self._allowed_math_functions = [
            ExpressionType.log,
            ExpressionType.exp,
            ExpressionType.sin,
            ExpressionType.cos,
            ExpressionType.tan,
        ]
        self._binary_op_lookup = {
            ExpressionType.add: "+",
            ExpressionType.sub: "-",
            ExpressionType.mul: r"\cdot",
            ExpressionType.pow: "^",
            ExpressionType.eq: "=",
            ExpressionType.neq: r"\neq",
            ExpressionType.leq: r"\leq",
            ExpressionType.geq: r"\geq",
        }

    def expression_to_latex_string(self, expr):
        assert self._stack == []
        self._walk(expr)
        ret = self._stack.pop()
        assert self._stack == []
        return ret

    @staticmethod
    def forall_object_to_latex_string(forall_obj):
        indices = [i.to_string() for i in forall_obj.indices_list()]
        if len(indices) == 1:
            indices_string = indices[0]
        else:
            indices_string = "(" + ",".join(indices) + ")"
        set_strings = " \\times ".join([s.name() for s in forall_obj.sets_list()])
        return rf"\forall_{{{indices_string} \in {set_strings}}}"

    def _visit(self, expr):
        if isinstance(expr, BinaryExprNode):
            right = self._stack.pop()
            left = self._stack.pop()
            if expr.operation in self._binary_op_lookup:
                op = self._binary_op_lookup[expr.operation]
                ret = f"{{{left}}} {op} {{{right}}}"
            elif expr.operation == ExpressionType.div:
                ret = f"\\frac{{{left}}}{{{right}}}"
            else:
                raise NotImplementedError(
                    f"Binary operation {expr.operation} not supported in ExpressionToLatexStringWalker"
                )
            self._stack.append(ret)
        elif isinstance(expr, UnaryExprNode):
            arg = self._stack.pop()
            if expr.operation not in self._allowed_math_functions:
                ret = rf"\texttt{{{expr.operation}}}({arg})"
            else:
                ret = rf"\{expr.operation}({arg})"
            self._stack.append(ret)
        elif isinstance(expr, ExprLeaf):
            if isinstance(expr, ComponentIndicesNode):
                ret = rf'{expr.component.name()}_{{{",".join([i.to_string() for i in expr.indices])}}}'
            else:
                ret = rf"{expr.to_string()}"
            self._stack.append(ret)
        elif isinstance(expr, SumExprNode):
            body = self._stack.pop()
            ret = (
                rf"\sum_{{{self.forall_object_to_latex_string(expr._forall)}}} ({body})"
            )
            self._stack.append(ret)
        elif isinstance(expr, ProdExprNode):
            body = self._stack.pop()
            ret = rf"\prod_{{{self.forall_object_to_latex_string(expr._forall)}}} ({body})"
            self._stack.append(ret)
        elif isinstance(expr, Expression):
            body = self._stack.pop()
            ret = rf"({body})"
            self._stack.append(ret)
        elif isinstance(expr, Objective):
            body = self._stack.pop()
            ret = rf"{body}"
            self._stack.append(ret)
        else:
            raise NotImplementedError(
                f"Expression node {expr} of type {type(expr)} not supported in ExpressionToLatexStringWalker"
            )


def expression_to_latex_string(expr):
    return ExpressionToLatexStringWalker().walk(expr)


def variable_to_latex_string(var):

    if var._domain == Reals:
        dom_str = f"\\mathbb{{R}}"
    elif var._domain == Binary:
        dom_str = "\\{0, 1\\}"
    else:
        raise NotImplementedError(
            f"Domain {var._domain} not supported in variable_to_latex_string"
        )

    if var._forall is None:
        return f"{var.name()} \\in {dom_str}"
    else:
        set_str = " \\times ".join([s.name() for s in var._forall.sets_list()])
        return f"{var.name()} \\in {dom_str}^{{|{set_str}|}}"


def model_to_latex_string(model):
    writer = LatexWriter()
    lines = [
        f"\\begin{{subequations}}",
        f"\\begin{{align}}",
        f"& \\text{{min}} && {writer._expr_writer.expression_to_latex_string(model.objective)} &&& \\\\",
    ]

    constr = model.constraints[0]
    lines.append(
        f'& \\text{{s.t.}} &&{writer._expr_writer.expression_to_latex_string(constr._expr)}, &&& {writer._expr_writer.                                   forall_object_to_latex_string(constr._forall) if constr._forall else ""}'
    )
    for constr in model.constraints[1:]:
        lines.append("\\")
        lines.append(
            f'& && {writer._expr_writer.expression_to_latex_string(constr._expr)}, &&& {writer._expr_writer.forall_object_to_latex_string(constr.        _forall) if constr._forall else ""}'
        )

    lines.append("\\\\")
    lines.append(
        "&&&"
        + ",".join([f"{variable_to_latex_string(c)}" for c in model.variables])
        + "&&&"
    )

    lines.append(f"\\end{{align}}")
    lines.append(f"\\end{{subequations}}")

    return "\n".join(lines)


class LatexWriter(object):

    def __init__(self):
        self._expr_writer = ExpressionToLatexStringWalker()

    def write_model(self, model, fname):
        with open(fname, "w") as fd:
            fd.writelines(
                [
                    f"\\documentclass{{article}}\n",
                    f"\\usepackage{{amsmath}}\n",
                    "\\usepackage{{amsfonts}}",
                    f"\\begin{{document}}\n",
                ]
            )

            fd.write(f"{model_to_latex_string(model)}")

            fd.writelines([f"\\end{{document}}"])

    # def write_model(self, fname, *args):
    #     file_path = os.path.dirname(os.path.abspath(__file__))
    #     templates_path = os.path.join(file_path, 'templates')
    #     environment = Environment(loader=FileSystemLoader(templates_path))
    #     template = environment.get_template("tex_template.tex")
    #     symbstr = ''
    #     constr = ''
    #     for c in args:
    #         if isinstance(c, Set) or isinstance(c, ScalarVariable) or isinstance(c, Parameter):
    #             if c.is_scalar():
    #                 symbstr += f'${c.name}$ & {c.doc}\\\\ \n'
    #             else:
    #                 indices = list(idx.name for idx in c._forall.indices_list())
    #                 indices = ','.join(indices)
    #                 symbstr += f'${c.name}_{{{indices}}}$ & {c.doc}\\\\ \n'
    #         elif isinstance(c, Expression):
    #             if c.is_scalar():
    #                 expr = expression_to_latex_string(c.expr)
    #                 constr += f'\\begin{{align}}\n{expr}\n\\end{{align}}\n'
    #             else:
    #                 expr = expression_to_latex_string(c.expr)
    #                 constr += f'\\begin{{align}}\n{expr} \;\; \forall i \in S\n\\end{{align}}\n'
    #         else:
    #             raise NotImplementedError(f'Unknown expression {expr} of type {type(expr)} in LatexWriter')

    #     content = template.render(symbols=symbstr, constraints=constr)
    #     with open(fname, mode="w", encoding="utf-8") as texfile:
    #         texfile.write(content)


# class LatexExpressionWalker(BottomUpDepthFirstExpressionWalker):
#     def __init__(self):
#         super().__init__()
#         self._symbols = dict()
#         self._str = ''
#         self._child_strs = list()

#     def latex_expression(self, expr):
#         self._walk(expr)
#         assert len(self._child_strs) == 1
#         return self._child_strs[0]

#     def _visit(self, expr):
#         if isinstance(expr, ComponentIndicesNode):
#             assert len(self._child_strs) == 0 or len(self._child_strs) == 1
#             indices = list(idx.name for idx in expr.indices)
#             indices = ','.join(indices)
#             self._child_strs.append(f'{expr.component.name}_{{{indices}}}')

#         elif isinstance(expr, ExprLeaf):
#             assert len(self._child_strs) == 0 or len(self._child_strs) == 1

#             self._child_strs.append(str(expr))
#         elif isinstance(expr, BinaryExprNode):
#             assert len(self._child_strs) == 2
#             opstr = self._latex_operation_str(expr.operation)
#             self._child_strs = [f'({self._child_strs[0]} {opstr} {self._child_strs[1]})']
#         elif isinstance(expr, SumExprNode):
#             self._child_strs = [f'(\sum_{{i \in S}} {self._child_strs[0]})']
#         else:
#             raise NotImplementedError(f'Expression node {expr} of type {type(expr)} not supported in BottomUpDepthFirstExpressionWalker')

#         print('visiting', str(expr))

#     def _latex_operation_str(self, op):
#         if op == '<=':
#             return '\le'
#         elif op == '>=':
#             return '\ge'
#         elif op == '*':
#             return ''
#         return op
