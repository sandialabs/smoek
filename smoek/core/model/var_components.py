from pyomo.common.collections import ComponentMap
from enum import Enum
from smoek.core.expr.forall import ForAllObject
from smoek.core.expr.nodes import (
    ExprLeaf,
    ComponentIndicesNode,
    ExpressionType,
    _wrap_expression_if_needed,
)
from .components import ModelingComponent, index


class Domain(Enum):
    Reals = 1
    Binary = 2
    Integers = 3


#
# Can specify domain using a class that specifies domain/lower/upper values
#
class DomainType(object):

    counter = 0

    def __init__(self, *, domain, lower, upper):
        self.id = DomainType.counter
        DomainType.counter = DomainType.counter + 1
        self.domain = domain
        self.lower = lower
        self.upper = upper

    def __eq__(self, dtype):
        return self.id == dtype.id

    def __neq__(self, dtype):
        return self.id != dtype.id


Reals = DomainType(domain=Domain.Reals, lower=None, upper=None)
PositiveReals = DomainType(domain=Reals, lower=0, upper=None)
NegativeReals = DomainType(domain=Reals, lower=None, upper=0)

Binary = DomainType(domain=Domain.Binary, lower=0, upper=1)

Integers = DomainType(domain=Domain.Integers, lower=None, upper=None)
PositiveIntegers = DomainType(domain=Integers, lower=1, upper=None)
NegativeIntegers = DomainType(domain=Integers, lower=None, upper=-1)
NonNegativeIntegers = DomainType(domain=Integers, lower=0, upper=None)
NonPositiveIntegers = DomainType(domain=Integers, lower=None, upper=0)


#
# TODO: I don't think we need to differentiate between ScalarVariable and IndexedVariable
# Calling variable().forall(...) will automatically create an indexed variable
# However, scalar vars need to inherit Expr Leaf while indexed need __getitem__ method
# WEH - So these are different...?
#
class ScalarVariable(ModelingComponent, ExprLeaf):
    def __init__(self, name=None, domain=None, doc=None):
        super().__init__(name, doc)
        if domain is not None:
            assert isinstance(domain, DomainType)
        else:
            domain = Reals
        self._domain = domain
        self._lower = None
        self._upper = None
        self._value = None
        self._fixed = False

    def value(self, value=None):
        if value is None:
            return self._value
        self._value = _wrap_expression_if_needed(value)
        return self

    def lower(self, value=None):
        if value is None:
            return self._lower
        self._lower = _wrap_expression_if_needed(value)
        return self

    def upper(self, value=None):
        if value is None:
            return self._upper
        self._upper = _wrap_expression_if_needed(value)
        return self

    def bounds(self, lower, upper):
        self._lower = _wrap_expression_if_needed(lower)
        self._upper = _wrap_expression_if_needed(upper)
        return self

    def domain(self, value=None):
        if value is None:
            return self._domain
        self._domain = value
        return self

    within = domain

    def fixed(self, value=None):
        if value is None:
            return self._fixed
        self._fixed = value == True
        return self

    def fix(self, value):
        self._value = _wrap_expression_if_needed(value)
        self._fixed = True
        return self

    def etype(self):
        return ExpressionType.variable

    def forall(self, *iset_pairs, explicit=True):
        res = IndexedVariable(
            forall=ForAllObject().forall(*iset_pairs),
            name=self.name(),
            domain=self._domain,
            doc=self._doc,
        )
        res._explicit = self._explicit and explicit
        return res

    def index_set(self, iset):
        return self.forall(index(f"i{len(self._index_sets())}") in iset, explicit=False)


def variable(name=None, domain=Reals, doc=None, forall=None):
    if forall is None:
        return ScalarVariable(name=name, domain=domain, doc=doc)
    else:
        return IndexedVariable(forall, name=name, domain=domain, doc=doc)


# WEH - Why are these only scalar?
def binary_variable(name=None, doc=None):
    return ScalarVariable(name=name, domain=Binary, doc=doc)


# WEH - Why are these only scalar?
def real_variable(name=None, doc=None):
    return ScalarVariable(name=name, domain=Reals, doc=doc)


class IndexedVariable(ModelingComponent):
    def __init__(self, forall, name=None, domain=None, doc=None):
        super().__init__(name, doc)
        if domain is not None:
            assert isinstance(domain, DomainType)
        self._domain = domain
        self._forall = forall
        self._component_indices = ComponentMap()
        self._lower = None
        self._upper = None
        self._value = None
        self._fixed = None

    def etype(self):
        return ExpressionType.variable

    def __getitem__(self, indices):
        if indices not in self._component_indices:
            self._component_indices[indices] = ComponentIndicesNode(self, indices)
        return self._component_indices[indices]

    def value(self, value=None):
        if value is None:
            return self._value
        self._value = _wrap_expression_if_needed(value)
        return self

    def lower(self, value=None):
        if value is None:
            return self._lower
        self._lower = _wrap_expression_if_needed(value)
        return self

    def upper(self, value=None):
        if value is None:
            return self._upper
        self._upper = _wrap_expression_if_needed(value)
        return self

    def bounds(self, lower, upper):
        self._lower = _wrap_expression_if_needed(lower)
        self._upper = _wrap_expression_if_needed(upper)
        return self

    def domain(self, value=None):
        if value is None:
            return self._domain
        self._domain = value
        return self

    def fixed(self, value=None):
        if value is None:
            return self._fixed
        self._fixed = value == True
        return self

    def fix(self, value):
        self._value = _wrap_expression_if_needed(value)
        self._fixed = True
        return self

    within = domain
