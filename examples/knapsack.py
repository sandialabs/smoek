# README
# 

import smoek as smk


def knapsack(N):
    N = N * 1000
    W = N / 10.0

    i = smk.index("i")

    # WEH - How would we initialize "INDEX" in this first case?  This is an abstract model that does not have
    #           enough data to generate an instance.
    #INDEX = smk.set("INDEX")

    N = smk.parameter("N")
    INDEX = smk.range("INDEX", N)           # 0..N-1
    #INDEX = smk.sequence("INDEX", N)        # 1..N

    w = smk.parameter()
           .name("w")
           .forall(i, In=INDEX)
           .value(1/W)
        #initialize=lambda model, i: random.uniform(0.0, 1.0),
        #within=smk.Domain.Reals,
    )

    v = smk.parameter("v").forall(i, In=INDEX).value(1)
        #initialize=lambda model, i: random.uniform(0.0, 1.0),
        #within=pe.Reals,

    x = smk.variable()
        .name("x")
        .forall(i, In=INDEX)
        .bounds(0.0,1.0)

    # o = smk.objective("o", expr=smk.sum(v[i] * x[i]).forall(i, In=INDEX))
    o = smk.objective()
         .name("o")
         .expr( smk.sum(v[i] * x[i]).forall(i, In=INDEX) )
         .minimize()
         
    c = smk.constraint("c", expr=smk.sum(w[i] * x[i]).forall(i, In=INDEX) <= W)

    return smk.model(minimize=o, constraints=[c], variables=[x], name="knapsack")


{'N': 10,
 'w': {0: 1/10,
       1: 1/10,
       2: 1/10
       },
 'v': {

M = knapsack(10)

import smoek.pyomo_instance_backend as pmo
instance = pmo.generate(M, data=my_data_dict)            # Should this be a method?   M.generate("pyomo")

import smoek.jump_backend as jmp
jmp.generate(M, data=my_data_dict, filename='foo.jmp')

import smoek.cpp_backend as cpp
cpp.generate(M)

import smoek.jax_backend as jx

#instance = generate(M, data=my_data_dict, backend='pyomo-instance')
import smoek.pyomo_source_backend as pmos
pmos.generate(M, fname='pyomo_knapsack.py', data_import_format='hd5')

# nice to have
python pyomo_knapsack.py foo.hd5

# not sure if this is the right format
from pyomo_knapsack import build_pyomo_model
foo = build_pyomo_model(data_dict)



#instance = generate_instance(M, "pycoek")

opt = smk.solver("gurobi")
res = opt.solve(instance)                           # Load solution into instance
res = opt.solve(instance, load_solutions=False)     # The 'res' object stores the solution, but 'instance' is not changed

