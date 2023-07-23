from smoek.core import index, set, parameter, forall, \
    variable, binary_variable, smoek_sum, constraint, objective
from smoek.io.tex import LatexWriter

def test_knapsack():
    i = index('i')
    A = set('A', doc=r'set of all items')
    v = parameter('v', forall(i, In=A), doc=r'value of item $i$')
    w = parameter('w', forall(i, In=A), doc=r'weight of item $i$')
    w_max = parameter(r'\bar w', doc=r'maximum weight')
    x = binary_variable('x', forall(i, In=A), doc='indicator variable for item selection')

    c = constraint(
        name='max_w_con',
        expr=smoek_sum(w[i]*x[i], forall(i, In=A)) <=  w_max,
        doc=r'weight limit'
        )

    o = objective(
        name='obj',
        expr=smoek_sum(v[i]*x[i], forall(i, In=A)),
        doc='maximize value objective'
        )

    l = LatexWriter()
    l.write_model('./tex/knapsack.tex', A, v, w, w_max, x, c, o)


if __name__ == '__main__':
    test_knapsack()
