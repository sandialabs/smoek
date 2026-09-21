import smoek.core as smk
from smoek.io.tex import LatexWriter

c = smk.index("c")
w = smk.index("w")

W = smk.set("W", doc=r"set of candidate warehouses")
C = smk.set("C", doc=r"set of all customers")
d = (
    smk.parameter("d", doc=r"distance from warehouse w to customer c")
    .forall(w, In=W)
    .forall(c, In=C)
)

x = smk.variable("x").forall(w, In=W).forall(c, In=C)

o = smk.objective(
    name="transport_cost",
    expr=smk.smoek_sum(d[w, c] * x[w, c]).forall(w, In=W).forall(c, In=C),
)

c = smk.constraint(name="demand_met", expr=(smk.smoek_sum(x[w, c]).forall(w, In=W) == 1)).forall(
    c, In=C
)

l = LatexWriter()
l.write_model("./tex/warehouse.tex", o, c, x, W, C)
