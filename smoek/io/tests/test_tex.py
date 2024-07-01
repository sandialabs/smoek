import smoek as smk
from smoek.io.tex import model_to_latex_string, LatexWriter
from pathlib import Path
currdir = str(Path(__file__).parent.absolute())

def test_knapsack():
    i = smk.index('i')
    A = smk.index_set('A', doc=r'set of all items')
    v = smk.parameter('v', doc=r'value of item $i$').forall(i, In=A)
    w = smk.parameter('w', doc=r'weight of item $i$').forall(i, In=A)
    w_max = smk.parameter(r'\bar w', doc=r'maximum weight')
    x = smk.binary_variable('x', doc='indicator variable for item selection').forall(i, In=A)

    c = smk.constraint(
        name='max_w_con',
        expr=smk.sum(w[i]*x[i]).forall(i, In=A) <=  w_max,
        doc=r'weight limit'
    )

    o = smk.objective(
        name='obj',
        expr=smk.sum(v[i]*x[i]).forall(i, In=A),
        doc='maximize value objective'
    )

    M = smk.model(o, [c], [x], "knapsack", "test_knapsack()")
    l = model_to_latex_string(M)
    assert l == """\\begin{subequations}
\\begin{align}
& \\text{min} && (\\sum_{\\forall_{(i) \\in A}} ({v_{i}} \\cdot {x_{i}})) &&& \\\\
& \\text{s.t.} &&{\\sum_{\\forall_{(i) \\in A}} ({w_{i}} \\cdot {x_{i}})} \\leq {\\bar w}, &&& 
\\\\
&&&x \\in \\{0, 1\\}^{|A|}&&&
\\end{align}
\\end{subequations}"""

