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

    def forall(self, *index):
        assert len(index) > 0
        if index[0] is True:
            assert len(ForAllObject._latest) == len(index), f"Expected only {len(index)} items in _latest but saw {len(ForAllObject._latest)}"
            index = ForAllObject._latest
            ForAllObject._latest = []

        assert (
            len(ForAllObject._latest) == 0
        ), f"Latest len: {len(ForAllObject._latest)},  Index Type: {type(index[0])}"
        if type(index) is list:
            for iset_pair in index:
                self._index_set_pairs.append(iset_pair)
        elif isinstance(index, IndexSetPair):
            self._index_set_pairs.append(index)
        else:
            assert False, "Unexpected type for forall(): {type(index)}"
            # self._index_set_pairs.append(IndexSetPair(index, In))
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


def forall(*index):
    return ForAllObject().forall(*index)
