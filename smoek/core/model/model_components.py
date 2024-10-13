from typing import List, Dict
from .var_components import ScalarVariable, IndexedVariable
from .constr_components import Constraint
from .var_components import ScalarVariable, IndexedVariable
from .constr_components import Constraint
from .expressions import Objective


class Model(object):
    def __init__(self, objective, constraints, variables, name="model", doc=""):
        self.objective = objective
        self.constraints: List[Constraint] = constraints
        self.variables: List[ScalarVariable | IndexedVariable] = variables
        self.name = name
        self.doc = doc

        # add names for model construction
        for i, c in enumerate(self.constraints):
            if c.name() is None:
                c.name(f"_c{i}")
        if not self.objective is None and self.objective.name() is None:
            self.objective.name(f"_o")
        for i, v in enumerate(self.variables):
            if v.name() is None:
                v.name(f"_v{i}")

    # This class enables the model() function to act as a parameterized
    # class decorator.
    #
    # WARNING: This method returns a new class that inherits from Model.  This assumes that
    # the Model attributes do not conflict with a user's attributes, which may not be
    # true!
    def __call__(self, cls):
        tmp = self

        class SmoekModel(Model, cls):

            def __init__(self, *args, **kwds):
                cls.__init__(self, *args, **kwds)
                objective, constraints, variables = _collect_components(self)
                Model.__init__(
                    self,
                    objective,
                    constraints,
                    variables,
                    name=cls.__name__ if tmp.name == "model" else tmp.name,
                    doc=tmp.doc,
                )

        return SmoekModel


def _collect_components(obj):
    objective = None
    constraints = []
    variables = []

    for k in dir(obj):
        if k.startswith("_"):
            continue
        v = getattr(obj, k)
        if isinstance(v, Objective):
            objective = v
        elif isinstance(v, Constraint):
            constraints.append(v)
        elif isinstance(v, ScalarVariable) or isinstance(v, IndexedVariable):
            variables.append(v)

    return objective, constraints, variables


def model(*, objective=None, constraints=None, variables=None, name="model", doc=""):
    objective = None if objective is None else objective
    constraints = [] if constraints is None else constraints
    variables = [] if variables is None else variables
    return Model(objective, constraints, variables, name=name, doc=doc)
