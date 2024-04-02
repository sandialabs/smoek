import os
import sympy as sp

from jinja2 import Environment, FileSystemLoader

# TODO: remove the reliance on types
from smoek.core.set_components import Set # ScalarSet, IndexedSet
from smoek.core.var_components import ScalarVariable # ScalarVariable, IndexedVariable
from smoek.core.expr_components import Expression, Constraint, Objective # ScalarExpression, IndexedExpression
from smoek.core.components import ComponentIndicesNode
from smoek.core.data_components import Parameter # ScalarParameter, IndexedParameter

from smoek.core.expression import ExprLeaf, BinaryExprNode
from smoek.core.utils import BottomUpDepthFirstExpressionWalker
from smoek.core.functions import SumExprNode

def _latex_expression(expr):
    w = LatexExpressionWalker()
    return w.latex_expression(expr)

class LatexWriter(object):
    def __init__(self):
        pass

    def write_model(self, fname, *args):
        file_path = os.path.dirname(os.path.abspath(__file__))
        templates_path = os.path.join(file_path, 'templates')
        environment = Environment(loader=FileSystemLoader(templates_path))
        template = environment.get_template("tex_template.tex")
        symbstr = ''
        constr = ''
        for c in args:
            if isinstance(c, Set) or isinstance(c, ScalarVariable) or isinstance(c, Parameter):
                if c.is_scalar():
                    symbstr += f'${c.name}$ & {c.doc}\\\\ \n'
                else:
                    indices = list(idx.name for idx in c._forall.indices_list())
                    indices = ','.join(indices)
                    symbstr += f'${c.name}_{{{indices}}}$ & {c.doc}\\\\ \n'
            elif isinstance(c, Expression):
                if c.is_scalar():
                    expr = _latex_expression(c.expr)
                    constr += f'\\begin{{align}}\n{expr}\n\\end{{align}}\n'
                else:
                    expr = _latex_expression(c.expr)
                    constr += f'\\begin{{align}}\n{expr} \;\; \forall i \in S\n\\end{{align}}\n'
            else:
                raise NotImplementedError(f'Unknown expression {expr} of type {type(expr)} in LatexWriter')

        content = template.render(symbols=symbstr, constraints=constr)
        with open(fname, mode="w", encoding="utf-8") as texfile:
            texfile.write(content)
    
    def _write_model(self, fname, *args):
        with open(fname, 'w') as fd:
            # write the notation table
            fd.write(r"""\documentclass{article}
\usepackage{amsmath}
\begin{document}
\begin{table}
\begin{tabular}{c|p{4in}}
Symbol & Description \\
\hline \hline
"""
                     )
                     
            for c in args:
                if isinstance(c, ScalarSet) or isinstance(c, ScalarVariable) or isinstance(c, ScalarParameter): 
                    fd.write(f'${c.name}$ & docs\\\\')
                elif isinstance(c, IndexedSet) or isinstance(c, IndexedVariable) or isinstance(c, IndexedParameter):
                    indices = 'i,j' #indices_list(c._forall)
                    fd.write(f'${c.name}_{{{indices}}}$ & docs\\\\')

            fd.write(r""" \\ \hline
\end{tabular}
\end{table}
\end{document}
""")
            

    
class LatexExpressionWalker(BottomUpDepthFirstExpressionWalker):
    def __init__(self):
        super().__init__()
        self._symbols = dict()
        self._str = ''
        self._child_strs = list()
        
    def latex_expression(self, expr):
        self._walk(expr)
        assert len(self._child_strs) == 1
        return self._child_strs[0]
    
    def _visit(self, expr):
        if isinstance(expr, ComponentIndicesNode):
            assert len(self._child_strs) == 0 or len(self._child_strs) == 1
            indices = list(idx.name for idx in expr.indices)
            indices = ','.join(indices)
            self._child_strs.append(f'{expr.component.name}_{{{indices}}}')
            
        elif isinstance(expr, ExprLeaf):
            assert len(self._child_strs) == 0 or len(self._child_strs) == 1

            self._child_strs.append(str(expr))
        elif isinstance(expr, BinaryExprNode):
            assert len(self._child_strs) == 2
            opstr = self._latex_operation_str(expr.operation)
            self._child_strs = [f'({self._child_strs[0]} {opstr} {self._child_strs[1]})']
        elif isinstance(expr, SumExprNode):
            self._child_strs = [f'(\sum_{{i \in S}} {self._child_strs[0]})']
        else:
            raise NotImplementedError(f'Expression node {expr} of type {type(expr)} not supported in BottomUpDepthFirstExpressionWalker')
        
        print('visiting', str(expr))

    def _latex_operation_str(self, op):
        if op == '<=':
            return '\le'
        elif op == '>=':
            return '\ge'
        elif op == '*':
            return ''
        return op
