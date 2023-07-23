from smoek.core import index, index_set, parameter, forall, \
    variable, binary_variable, smoek_sum, constraint, objective
from smoek.core.writers import LatexWriter

def test_knapsack():
    i = index('i')
    A = index_set('A')
    v = parameter('v', forall(i, In=A))
    w = parameter('w', forall(i, In=A))
    w_max = parameter(r'\bar w')
    x = binary_variable('x', forall(i, In=A))

    c = constraint(
        'max_w_con',
        smoek_sum(w[i]*x[i], forall(i, In=A)) <=  w_max
        )

    o = objective(
        'obj',
        smoek_sum(v[i]*x[i], forall(i, In=A))
        )

    l = LatexWriter()
    l.write_model('./tex/knapsack.tex', A, v, w, w_max, x, c, o)

if __name__ == '__main__':
    test_knapsack()
