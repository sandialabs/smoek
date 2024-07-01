import smoek as smk


def knapsack(N):
    N = N * 1000
    W = N / 10.0

    i = smk.index("i")

    # WEH - How would we initialize "INDEX" in this first case?  This is an abstract model that does not have
    #           enough data to generate an instance.
    #INDEX = smk.set("INDEX")

    INDEX = smk.range("INDEX", N)           # 0..N-1
    #INDEX = smk.sequence("INDEX", N)        # 1..N

    w = smk.parameter("w").forall(i, In=INDEX).value(1/W)
        #initialize=lambda model, i: random.uniform(0.0, 1.0),
        #within=smk.Domain.Reals,
    )

    v = smk.parameter("v").forall(i, In=INDEX).value(1)
        #initialize=lambda model, i: random.uniform(0.0, 1.0),
        #within=pe.Reals,

    x = smk.variable("x").forall(i, In=INDEX).bounds(0.0,1.0)

    o = smk.objective("o", expr=smk.sum(v[i] * x[i]).forall(i, In=INDEX))

    c = smk.constraint("c", expr=smk.sum(w[i] * x[i]).forall(i, In=INDEX) <= W)

    return smk.model(minimize=o, constraints=[c], variables=[x], name="knapsack")


M = knapsack(10)
instance = generate_instance(M, "pyomo")            # Should this be a method?   M.generate("pyomo")
#instance = generate_instance(M, "pycoek")

opt = smk.solver("gurobi")
res = opt.solve(instance)                           # Load solution into instance
res = opt.solve(instance, load_solutions=False)     # The 'res' object stores the solution, but 'instance' is not changed

