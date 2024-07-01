from .expr_components import ComponentIndicesNode

# todo: error checking
# todo: augment printing

# TODO: change these classes so that all components are the same
# and the presence of forall indicates that they are indexed


class IndexSetPair(object):
    def __init__(self, index, index_set):
        self._index = index
        self._set = index_set

    @property
    def index(self):
        return self._index

    @property
    def set(self):
        return self._set


class ForAllObject(object):
    def __init__(self):
        self._index_set_pairs = list()
        self._filter_expressions = list()

    def forall(self, index, In=None):
        self._index_set_pairs.append(IndexSetPair(index, In))
        return self

    def suchthat(self, expr):
        self._filter_expressions.append(expr)
        return self

    def indices_list(self):
        return list(isp.index for isp in self._index_set_pairs)

    def sets_list(self):
        return list(isp.set for isp in self._index_set_pairs)

    def to_string(self):
        ret = "forall " + ", ".join(
            [
                f"{isp.index.to_string()} in {isp.set.name}"
                for isp in self._index_set_pairs
            ]
        )
        return ret


def forall(index, In=None):
    return ForAllObject().forall(index, In=In)


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
