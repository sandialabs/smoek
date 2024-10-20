from typing import List, Dict
from .var_components import ScalarVariable, IndexedVariable
from .constr_components import Constraint
from .var_components import ScalarVariable, IndexedVariable
from .constr_components import Constraint
from .expressions import Objective


def _smoek_model(cls, name=None, doc=""):
    class SmoekModel(Model, cls):

        def __init__(self, *args, **kwds):
            cls.__init__(self, *args, **kwds)
            objective, constraints, variables = _collect_components(self)
            Model.__init__(
                self,
                objective,
                constraints,
                variables,
                name=cls.__name__ if name is None else name,
                doc=doc,
            )

    return SmoekModel


class Model(object):
    def __init__(self, objective, constraints, variables, name=None, doc=""):
        self.objective = objective
        self.constraints: List[Constraint] = constraints
        self.variables: List[ScalarVariable | IndexedVariable] = variables
        self.name = "model" if name is None else name
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
        name_ = self.name if self.name != "model" else None
        return _smoek_model(cls, name=name_, doc=self.doc)


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


def model(*args, objective=None, constraints=None, variables=None, name=None, doc=""):
    if len(args) > 0:
        return _smoek_model(args[0], name=name, doc=doc)
    else:
        objective = None if objective is None else objective
        constraints = [] if constraints is None else constraints
        variables = [] if variables is None else variables
        return Model(objective, constraints, variables, name=name, doc=doc)
