import smoek.core as smk
import numpy as np
from smoek.io.tex import expression_to_latex_string, LatexWriter

# indices
i = smk.index('i')
j = smk.index('j')

# index sets, contents/constructiuon not defined
# should there be a data attribute?
I = smk.set('I')
J = smk.set('J')

# indexed sets, contents/constructiuon not defined
S = smk.set('S').forall(i, In=I).suchthat(i >= 0)


M = smk.parameter('M').forall(i, In=I).forall(j, In=J)


v = smk.variable(name='v').forall(i, In=S)
x = smk.variable(name='x').forall(j, In=J)
z = smk.variable(name='z', domain=smk.Domain.Binary).forall(i, In=S)

c1 = smk.constraint(expr = 32 * v[i] - smk.sin(x[j] + 4) >= 0, name='c1').forall(i, In=S).forall(j, In=J)

c2 = smk.constraint(expr = M[i, j] / x[j] <= v[i] * z[i], name='c2').forall(i, In=I).forall(j, In=J)

c3 = smk.constraint(expr = smk.sin(3) / smk.sum(v[i]**2 + x[j]**2).forall(i, In=I).forall(j, In=J) <= 100, name='c3')

# print(smk.to_string(c1._expr))
# print(smk.to_list(c1._expr))
print(c1.to_string())
print(c2.to_string())
print(c3.to_string())
print(smk.utils.expr_to_string(c1._expr))
print(smk.utils.expr_to_string(c2._expr))
print(smk.utils.expr_to_string(c3._expr))

print(expression_to_latex_string(c1._expr))
print(expression_to_latex_string(c2._expr))
print(expression_to_latex_string(c3._expr))

# print(smk.utils.expr_to_list(c1._expr))
# print(smk.utils.expr_to_list(c2._expr))
# print(smk.utils.expr_to_list(c3._expr))

#ex1 = smk.expression(name='ex1', expr=v[i]**3 + smk.sin(x[i] + 4)).forall(i, In=I)
# ex2 = smk.expression(name='ex2', expr=3 * ex1)
# print(smk.utils.expr_to_string(ex2))

m = smk.model(minimize = smk.sum(v[i]**2 + x[j]**2).forall(i, In=I).forall(j, In=J),
              #minimize = ex1[i],
              constraints=[c1, c2, c3],
              variables=[v, x, z],
              name='m')

LatexWriter()._write_model(m, 'examples/tex/model.tex')



