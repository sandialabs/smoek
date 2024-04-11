


class Model:
    def __init__(self, objective, constraints, variables,  name=None, doc=None):
        self.objective = objective
        self.constraints = constraints
        self.variables = variables
        self.name = name
        self.doc = doc



def model(minimize, constraints, variables, name=None, doc=None):
    return Model(minimize, constraints, variables, name=name, doc=doc)