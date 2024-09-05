from pyomo.common.collections import ComponentMap
from enum import Enum
from munch import Munch
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
# Can specify domain using a Munch that specifies domain/lower/upper values
#
Reals = Munch(domain=Domain.Reals, lower=None, upper=None)
PositiveReals = Munch(domain=Reals, lower=0, upper=None)
NegativeReals = Munch(domain=Reals, lower=None, upper=0)

Binary = Munch(domain=Domain.Binary, lower=0, upper=1)

Integers = Munch(domain=Domain.Integers, lower=None, upper=None)
PositiveIntegers = Munch(domain=Integers, lower=1, upper=None)
NegativeIntegers = Munch(domain=Integers, lower=None, upper=-1)
NonNegativeIntegers = Munch(domain=Integers, lower=0, upper=None)
NonPositiveIntegers = Munch(domain=Integers, lower=None, upper=0)


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
            assert isinstance(domain, Domain)
        else:
            domain = Domain.Reals
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

    fix = fixed

    def etype(self):
        return ExpressionType.variable

    def forall(self, index, In):
        res = IndexedVariable(
            forall=ForAllObject().forall(index, In),
            name=self.name(),
            domain=self._domain,
            doc=self._doc,
        )
        return res

    def index_set(self, In):
        return self.forall(index("i"), In=In)


def variable(name=None, domain=Domain.Reals, doc=None, forall=None):
    if forall is None:
        return ScalarVariable(name=name, domain=domain, doc=doc)
    else:
        return IndexedVariable(forall, name=name, domain=domain, doc=doc)


# WEH - Why are these only scalar?
def binary_variable(name=None, doc=None):
    return ScalarVariable(name=name, domain=Domain.Binary, doc=doc)


# WEH - Why are these only scalar?
def real_variable(name=None, doc=None):
    return ScalarVariable(name=name, domain=Domain.Reals, doc=doc)


class IndexedVariable(ModelingComponent):
    def __init__(self, forall, name=None, domain=None, doc=None):
        super().__init__(name, doc)
        if domain is not None:
            assert isinstance(domain, Domain)
        self._domain = domain
        self._forall = forall
        self._component_indices = ComponentMap()
        self._lower = None
        self._upper = None
        self._value = None

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
