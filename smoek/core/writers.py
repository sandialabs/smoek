from smoek.core.set_components import ScalarSet, IndexedSet
from smoek.core.var_components import ScalarVariable, IndexedVariable
from smoek.core.components import ScalarConstraint, IndexedConstraint
from smoek.core.components import ScalarObjective, IndexedObjective
from smoek.core.data_components import ScalarParameter, IndexedParameter

class LatexWriter(object):
    def __init__(self):
        pass

    def write_model(self, fname, *args):
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
            

    
