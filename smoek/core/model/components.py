from smoek.core.expr.forall import ForAllObject
from smoek.core.expr.nodes import ComponentIndicesNode

# todo: error checking
# todo: augment printing


class NamedComponent(object):
    def __init__(self, name=None, doc=None):
        # TODO: add rules for supplied names, i.e. no spaces, no special characters
        # and some exclusion for defult names, e.g. no '_' as first character.
        # also list of forbidden names, e.g. 'forall', 'in', 'suchthat'
        self._name = name
        self._doc = doc

    @property
    def name(self):
        assert self._name is not None, "No name specified for this component"
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, doc):
        self._doc = doc

    def __str__(self):
        if self._name is None:
            return "UnnamedComponent"
        return self._name


class ModelingComponent(NamedComponent):
    def __init__(self, name=None, doc=None):
        super().__init__(name, doc)
        self._forall = None

    def is_scalar(self):
        return self._forall is None

    def is_indexed(self):
        return self._forall is not None

    def forall(self, index, In):
        if self._forall is None:
            self._forall = ForAllObject()
        self._forall.forall(index, In=In)
        return self

    def suchthat(self, expr):
        # TODO: proper error message
        assert self._forall is not None
        self._forall.suchthat(expr)
        return self

    def __getitem__(self, indices):
        # TODO: proper error message
        assert self._forall is not None
        return ComponentIndicesNode(self, indices)

    # TODO: Decide whether to_string method should be in ModelingComponent classes,
    # or in a ComponentPrinter class which is specific to output format.
    # Could also use Mixins to add to_string method to ModelingComponents.
    # WEH: Alternatively, this could be an external function and not a method
    def to_string(self):
        # raise NotImplementedError('Derived classes must implement this')
        if self._forall is None:
            return f"{self._name}"
        else:
            return f"{self._name}, {self._forall.to_string()}"
