from smoek.core.expr.forall import ForAllObject
from smoek.core.expr.nodes import ComponentIndicesNode, ExprLeaf

# todo: error checking
# todo: augment printing


class GlobalComponentData(object):
    id = 0


class NamedComponent(object):

    def __init__(self, name=None, doc=None):
        # TODO: add rules for supplied names, i.e. no spaces, no special characters
        # and some exclusion for defult names, e.g. no '_' as first character.
        # also list of forbidden names, e.g. 'forall', 'in', 'suchthat'
        self._name = name
        self._doc = doc
        self._id = GlobalComponentData.id
        GlobalComponentData.id = GlobalComponentData.id + 1

    def name(self, name=None):
        if name is None:
            # assert self._name is not None, "No name specified for this component"
            return self._name
        self._name = name
        return self

    def doc(self, doc=None):
        if doc is None:
            return self._doc
        self._doc = doc
        return self

    def __str__(self):
        if self._name is None:
            return "UnnamedComponent"
        return self._name


# should we include attribute for dimension of index?
# can indices be ExprLeafs (e.g. for construction of filter expressions based on value)?
# would imply all indices are numeric - may be a sensible restriction
class Index(NamedComponent, ExprLeaf):
    def __init__(self, name=None):
        super().__init__(name=name)

    def to_string(self):
        return str(self)


# class NumericIndex(Index, ExprLeaf):
#     def __init__(self, name=None):
#         super().__init__(name=name)


def index(name=None):
    return Index(name)


class ModelingComponent(NamedComponent):
    def __init__(self, name=None, doc=None):
        super().__init__(name, doc)
        self._forall = None
        self._explicit = (
            True  # If True, then all indices have been provided for all index sets
        )

    def is_component(self):
        return True

    def is_scalar(self):
        return self._forall is None

    def is_indexed(self):
        return self._forall is not None

    @property
    def explicit(self):
        return self._forall is not None and self._explicit

    def forall(self, *iset_pairs, explicit=True):
        self._explicit = self._explicit and explicit
        if self._forall is None:
            self._forall = ForAllObject()
        self._forall.forall(*iset_pairs)
        return self

    def index_set(self, iset):
        return self.forall(index(f"i{len(self._index_sets())}") in iset, explicit=False)

    def suchthat(self, expr):
        assert self._forall is not None
        self._forall.suchthat(expr)
        return self

    def __getitem__(self, indices):
        assert self._forall is not None
        return ComponentIndicesNode(self, indices)

    def to_string(self):
        if self._forall is None:
            return f"{self._name}"
        else:
            return f"{self._name}, {self._forall.to_string()}"

    def __str__(self):
        return self.to_string()

    def _index_sets(self):
        # Return a list of the index sets used with this component
        if self._forall is None:
            return []
        return self._forall.sets_list()

    def _indices(self):
        # Return a list of the indices used with this component
        if self._forall is None:
            return []
        return self._forall.indices_list()

    def _index_set_pairs(self):
        if self._forall is None:
            return []
        return [isp for isp in self._forall._index_set_pairs]

    def _dependencies(self):
        # Return a list of the names of components that this component depends on
        return []
