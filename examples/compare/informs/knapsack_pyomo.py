
import pyomo.environ as pyo

def pow(a,b):
    return a**b

def generate_knapsack(data):
    M = pyo.ConcreteModel("knapsack")

    M.ITEMS = pyo.Set(initialize=data["ITEMS"])

    M.value = pyo.Param(M.ITEMS, mutable=True, within=pyo.Reals)

    M.weight = pyo.Param(M.ITEMS, mutable=True, within=pyo.Reals)

    M.capacity = pyo.Param(mutable=True, within=pyo.Reals)

    M.x = pyo.Var(M.ITEMS, bounds=(0.0,1.0))

    M.o = pyo.Objective(expr=sum(M.value[i] * M.x[i] for i in M.ITEMS))

    M.c = pyo.Constraint(expr=sum(M.weight[i] * M.x[i] for i in M.ITEMS) <= M.capacity)

    return M
