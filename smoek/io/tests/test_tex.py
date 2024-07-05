import smoek as smk
from smoek.io.tex import model_to_latex_string, LatexWriter
from pathlib import Path

currdir = str(Path(__file__).parent.absolute())


def test_knapsack():
    i = smk.index("i")
    A = smk.index_set("A", doc=r"set of all items")
    v = smk.parameter("v").forall(i, In=A).doc(r"value of item $i$")
    w = smk.parameter("w").forall(i, In=A).doc(r"weight of item $i$")
    w_max = smk.parameter(r"\bar w").doc(r"maximum weight")
    x = (
        smk.binary_variable("x")
        .forall(i, In=A)
        .doc("indicator variable for item selection")
    )

    c = (
        smk.constraint("max_w_con")
        .expr(smk.sum(w[i] * x[i]).forall(i, In=A) <= w_max)
        .doc(r"weight limit")
    )

    o = (
        smk.objective("obj")
        .expr(smk.sum(v[i] * x[i]).forall(i, In=A))
        .doc("maximize value objective")
    )

    M = smk.model(o, [c], [x], "knapsack", "test_knapsack()")
    l = model_to_latex_string(M)
    assert (
        l
        == """\\begin{subequations}
\\begin{align}
& \\text{min} && (\\sum_{\\forall_{(i) \\in A}} ({v_{i}} \\cdot {x_{i}})) &&& \\\\
& \\text{s.t.} &&{\\sum_{\\forall_{(i) \\in A}} ({w_{i}} \\cdot {x_{i}})} \\leq {\\bar w}, &&& 
\\\\
&&&x \\in \\{0, 1\\}^{|A|}&&&
\\end{align}
\\end{subequations}"""
    )
