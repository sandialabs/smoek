import smoek.core as smc
#from smoek.core import index, set, parameter, forall, \
#    variable, binary_variable, smoek_sum, constraint, objective
from smoek.io.tex import LatexWriter

def test_knapsack():
    i = smc.index('i')
    A = smc.set('A', doc=r'set of all items')
    v = smc.parameter('v', doc=r'value of item $i$').forall(i, In=A)
    w = smc.parameter('w', doc=r'weight of item $i$').forall(i, In=A)
    w_max = smc.parameter(r'\bar w', doc=r'maximum weight')
    x = smc.binary_variable('x', doc='indicator variable for item selection').forall(i, In=A)

    c = smc.constraint(
        name='max_w_con',
        expr=smc.smoek_sum(w[i]*x[i]).forall(i, In=A) <=  w_max,
        doc=r'weight limit'
    )

    o = smc.objective(
        name='obj',
        expr=smc.smoek_sum(v[i]*x[i]).forall(i, In=A),
        doc='maximize value objective'
    )

    l = LatexWriter()
    l.write_model('./tex/knapsack.tex', A, v, w, w_max, x, c, o)


if __name__ == '__main__':
    test_knapsack()
