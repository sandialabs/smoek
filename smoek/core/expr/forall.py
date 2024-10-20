from .nodes import ComponentIndicesNode

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

    _latest = []

    def __init__(self):
        self._index_set_pairs = list()
        self._filter_expressions = list()

    def forall(self, index, In=None):
        if index is True:
            assert len(ForAllObject._latest) > 0
            self._index_set_pairs.append(ForAllObject._latest.pop())
        else:
            self._index_set_pairs.append(IndexSetPair(index, In))
        return self

    def suchthat(self, expr):
        self._filter_expressions.append(expr)
        return self

    def indices_list(self):
        return [isp.index for isp in self._index_set_pairs]

    def sets_list(self):
        return [isp.set for isp in self._index_set_pairs]

    def to_string(self):
        ret = "forall " + ", ".join(
            [
                f"{isp.index.to_string()} in {isp.set.name()}"
                for isp in self._index_set_pairs
            ]
        )
        return ret


def forall(index, In=None):
    return ForAllObject().forall(index, In=In)
