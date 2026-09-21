from typing import List, Dict
from .components import NamedComponent, Index
from .var_components import ScalarVariable, IndexedVariable
from .data_components import Parameter, Data
from .set_components import Set
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

        def __setattr__(self, name, value):
            if isinstance(value, NamedComponent) and name not in [
                "objective",
                "constraints",
                "variables",
                "name",
                "doc",
            ]:
                value.name(name)
            super(SmoekModel, self).__setattr__(name, value)

    return SmoekModel


class Model(object):
    def __init__(self, objective, constraints, variables, name=None, doc=""):
        self._initialize(objective, constraints, variables, name, doc)

    def _update_smoek_components(self):
        objective, constraints, variables = _collect_components(self)
        self._initialize(objective, constraints, variables, self.name, self.doc)

    def _initialize(self, objective, constraints, variables, name=None, doc=""):
        # TODO - Use '_' variables for non-public Model data
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


def _set_name(obj, name):
    if obj.name() is None:
        obj.name(name)


def _collect_components(obj):
    objective = None
    constraints = []
    variables = []

    for k in dir(obj):
        if k.startswith("_"):
            continue
        if k in ["objective", "constraints", "variables", "doc", "name"]:
            continue

        v = getattr(obj, k)
        if isinstance(v, Objective):
            _set_name(v, k)
            objective = v
        elif isinstance(v, Constraint):
            _set_name(v, k)
            constraints.append(v)
        elif type(v) is list:
            for i, item in enumerate(v):
                assert isinstance(item, Constraint), f"Unexpected list element {type(item)}"
                _set_name(item, f"{k}[{i}]")
                constraints.append(item)
        elif isinstance(v, ScalarVariable) or isinstance(v, IndexedVariable):
            _set_name(v, k)
            variables.append(v)
        elif isinstance(v, Parameter):
            _set_name(v, k)
        elif isinstance(v, Data):
            _set_name(v, k)
        elif isinstance(v, Set):
            _set_name(v, k)
        elif isinstance(v, Index):
            _set_name(v, k)

    return objective, constraints, variables


def model(*args, objective=None, constraints=None, variables=None, name=None, doc=""):
    if len(args) > 0:
        return _smoek_model(args[0], name=name, doc=doc)
    else:
        objective = None if objective is None else objective
        constraints = [] if constraints is None else constraints
        variables = [] if variables is None else variables
        return Model(objective, constraints, variables, name=name, doc=doc)
