import smoek as smk

@smk.model
class knapsack:

    ITEMS = smk.set("ITEMS")

    i = smk.index("i")

    value = smk.parameter("value").index_set(ITEMS)

    weight = smk.parameter("weight").index_set(ITEMS)

    capacity = smk.parameter("capacity")

    x = smk.variable("x").index_set(ITEMS).bounds(0.0, 1.0)

    o = smk.objective("o").maximize(smk.sum(value[i] * x[i]).forall(i, In=ITEMS))

    c = smk.constraint("c").expr(
        smk.sum(weight[i] * x[i]).forall(i, In=ITEMS) <= capacity
    )


from smoek.io.tex import LatexWriter
writer = LatexWriter()
writer.write_model(knapsack(), "knapsack.tex")

from smoek.code.pyomo import generate
generate(model=knapsack(), outfile="knapsack_pyomo.py")

from smoek.code.coek import generate
generate(model=knapsack(), outfile="knapsack_coek.cpp")
