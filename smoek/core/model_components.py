from typing import List, Dict
from smoek.core.var_components import ScalarVariable, IndexedVariable
from smoek.core.constr_components import Constraint


class Model:
    def __init__(self, objective, constraints, variables, name="model", doc=""):
        self.objective = objective
        self.constraints: List[Constraint] = constraints
        self.variables: List[ScalarVariable | IndexedVariable] = variables
        self.name = name
        self.doc = doc

        # add names for model construction
        for i, c in enumerate(self.constraints):
            if c.name is None:
                c.name = f"_c{i}"
        for i, v in enumerate(self.variables):
            if v.name is None:
                v.name = f"_v{i}"


def model(minimize, constraints, variables, name="model", doc=""):
    return Model(minimize, constraints, variables, name=name, doc=doc)
