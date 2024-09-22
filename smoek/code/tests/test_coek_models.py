import pytest
import smoek as smk
from smoek.core.tests import models
from smoek.code.coek import generate


def test_small1():
    model = models.small1()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_small1(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("small1");

auto x = coek::variable("x").value(1.0);
model.add(x);

auto y = coek::variable("y").value(1.0);
model.add(y);

auto o = coek::objective("o").expr(coek::pow(x, 2));
model.add(o);

auto c = coek::constraint("c").expr(coek::pow(y, 2) == 4);
model.add(c);

return model;
}
"""
    )

def test_small2():
    model = models.small2()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_small2(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("small2");

auto x = coek::variable("x").value(1.0);
model.add(x);

auto y = coek::variable("y").value(1.0);
model.add(y);

auto o = coek::objective("o").expr(x);
model.add(o);

auto c = coek::constraint("c").expr(coek::pow(y, 2) == 4);
model.add(c);

return model;
}
"""
    )

def test_small3():
    model = models.small3()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_small3(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("small3");

auto x = coek::variable("x").value(1.0);
model.add(x);

auto y = coek::variable("y").value(1.0);
model.add(y);

auto o = coek::objective("o").expr((-(x * y)));
model.add(o);

auto c = coek::constraint("c").expr(coek::pow(y, 2) == 4);
model.add(c);

return model;
}
"""
    )

def test_small4():
    model = models.small4()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_small4(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("small4");

auto x = coek::variable("x").value(1.0);
model.add(x);

auto y = coek::variable("y").value(1.0);
model.add(y);

auto o = coek::objective("o").expr(coek::pow(y, 2));
model.add(o);

auto c = coek::constraint("c").expr(y * x == 4);
model.add(c);

return model;
}
"""
    )

def test_small5():
    model = models.small5()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_small5(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("small5");

auto x = coek::variable("x").lower(-1).upper(1).value(1.0);
model.add(x);

auto y = coek::variable("y").lower(-1).upper(2).value(2.0);
model.add(y);

auto v = coek::variable("v").lower(-1).upper(3).value(3.0);
model.add(v);

auto q = coek::parameter("q").value(2);

auto _o = coek::objective("_o").expr((coek::pow(x, 2) / 2.0) + (coek::pow(x, 2) / q));
model.add(_o);

auto _c0 = coek::constraint("_c0").expr((0.5 * v) * (x - y) == 2);
model.add(_c0);

auto _c1 = coek::constraint("_c1").expr((v / 2.0) * (x - y) == 2);
model.add(_c1);

auto _c2 = coek::constraint("_c2").expr((v * (x - y)) / 2.0 == 2);
model.add(_c2);

auto _c3 = coek::constraint("_c3").expr(v * ((x / 2.0) - (y / 2.0)) == 2);
model.add(_c3);

auto _c4 = coek::constraint("_c4").expr((v * (x - y)) * 0.5 == 2);
model.add(_c4);

auto _c5 = coek::constraint("_c5").expr(v * (x - y) == 4.0);
model.add(_c5);

auto _c6 = coek::constraint("_c6").expr(((1 / q) * v) * (x - y) == 2);
model.add(_c6);

auto _c7 = coek::constraint("_c7").expr((v / q) * (x - y) == 2);
model.add(_c7);

auto _c8 = coek::constraint("_c8").expr((v * (x - y)) / q == 2);
model.add(_c8);

auto _c9 = coek::constraint("_c9").expr(v * ((x / 2.0) - (y / q)) == 2);
model.add(_c9);

auto _c10 = coek::constraint("_c10").expr((v * (x - y)) * (1 / q) == 2);
model.add(_c10);

auto _c11 = coek::constraint("_c11").expr(v * (x - y) == 2 * q);
model.add(_c11);

return model;
}
"""
    )

def test_small6():
    model = models.small6()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_small6(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("small6");

auto _v0 = coek::variable("_v0").lower(-1).upper(1).value(1);
model.add(_v0);

auto _v1 = coek::variable("_v1").lower(-1).upper(2).value(2);
model.add(_v1);

auto _v2 = coek::variable("_v2").lower(-1).upper(3).value(3);
model.add(_v2);

auto _v3 = coek::variable("_v3").value(2);
model.add(_v3);

auto _o = coek::objective("_o").expr(_v0);
model.add(_o);

auto _c0 = coek::constraint("_c0").expr(((1 / _v3) * _v2) * (_v0 - _v1) == 2);
model.add(_c0);

auto _c1 = coek::constraint("_c1").expr((_v2 / _v3) * (_v0 - _v1) == 2);
model.add(_c1);

auto _c2 = coek::constraint("_c2").expr((_v2 * (_v0 - _v1)) / _v3 == 2);
model.add(_c2);

auto _c3 = coek::constraint("_c3").expr(_v2 * ((_v0 / _v3) - (_v1 / _v3)) == 2);
model.add(_c3);

auto _c4 = coek::constraint("_c4").expr((_v2 * (_v0 - _v1)) * (1 / _v3) == 2);
model.add(_c4);

auto _c5 = coek::constraint("_c5").expr(_v2 * (_v0 - _v1) == 2 * _v3);
model.add(_c5);

return model;
}
"""
    )

def test_testing1():
    model = models.testing1()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_testing1(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("testing1");

auto a = coek::variable("a").lower(0).upper(1).value(0);
model.add(a);

auto b = coek::variable("b").lower(0).upper(1).value(0);
model.add(b);

auto _v2 = coek::variable("_v2").lower(0);
model.add(_v2);

auto _v3 = coek::variable("_v3").upper(0);
model.add(_v3);

auto e = coek::variable("e").value(1.0);
model.add(e);

auto q = coek::parameter("q").value(2);

auto _o = coek::objective("_o").expr((3 * a) + q);
model.add(_o);

auto _c0 = coek::constraint("_c0").expr(((3 * b) + q) - a <= 0);
model.add(_c0);

auto _c1 = coek::constraint("_c1").expr((3 * b) + b == 0);
model.add(_c1);

auto _c2 = coek::constraint("_c2").expr(((((3 * b) * a) + q) + (b * b)) + (b * b) == 0);
model.add(_c2);

auto _c3 = coek::constraint("_c3").expr(((((3 * b) * b) + q) - (a * b)) - (a * a) <= 0);
model.add(_c3);

auto _c4 = coek::constraint("_c4").expr(coek::inequality(-7, ((((3 * b) * b) + q) - (a * b)) - (a * a), 7));
model.add(_c4);

auto _c5 = coek::constraint("_c5").expr(_v2 + _v3 == 0);
model.add(_c5);

auto _c6 = coek::constraint("_c6").expr(e + (3 * _v3) == 1);
model.add(_c6);

auto _c7 = coek::constraint("_c7").expr(coek::inequality(7, ((3 * b) + q) - a, 7));
model.add(_c7);

return model;
}
"""
    )

def test_testing2():
    model = models.testing2()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_testing2(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("testing2");

auto a = coek::variable("a").lower(0).upper(2).value(0);
model.add(a);

auto b = coek::variable("b").lower(0).upper(1).value(1.0);
model.add(b);

auto q = coek::parameter("q").value(2);

auto _o = coek::objective("_o").expr((((3 * a) + q) + (((a * a) * a) * ((((-a) + b) + (3 * a)) + (3 * b)))) + coek::sin((-coek::cos(a))));
model.add(_o);

return model;
}
"""
    )

# TODO: smk.expression()
def Xtest_testing3():
    model = models.testing3()

    assert (
        generate(model=model)
        == """
foo
"""
    )

def test_testing4():
    model = models.testing4()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_testing4(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("testing4");

auto x = coek::variable("x").lower(0).upper(1).value(0);
model.add(x);

auto y = coek::variable("y").lower(0).upper(1).value(0);
model.add(y);

auto z = coek::variable("z").lower(0).upper(1).value(0);
model.add(z);

auto a = coek::variable("a").lower(0).upper(1).value(0);
model.add(a);

auto b = coek::variable("b").lower(0).upper(1).value(0);
model.add(b);

auto _o = coek::objective("_o").expr((a + coek::cos(x)) + coek::cos(y));
model.add(_o);

auto _c0 = coek::constraint("_c0").expr((b + coek::cos(y)) + coek::cos(z) == 1);
model.add(_c0);

return model;
}
"""
    )

def test_testing5():
    model = models.testing5()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_testing5(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("testing5");

auto x = coek::variable("x").lower(2).upper(2);
model.add(x);

auto o = coek::objective("o").expr(x);
model.add(o);

return model;
}
"""
    )

def test_testing6():
    model = models.testing6()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_testing6(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("testing6");

auto x = coek::variable("x").lower(0).upper(1).value(0);
model.add(x);

auto p = coek::parameter("p").value(0);

auto q = coek::parameter("q").value(2);

auto o = coek::objective("o").expr((((-q) * x) * x) + p);
model.add(o);

return model;
}
"""
    )

def test_testing7():
    model = models.testing7()

    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_testing7(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("testing7");

auto A = coek::RangeSet(0, 3);

auto B = coek::RangeSet(0, 4);

auto i = coek::set_element("i");

auto j = coek::set_element("j");

auto p = coek::parameter("p").value(0);

auto pp = coek::parameter("pp", A).value(0);

auto ppp = coek::parameter("ppp", A*B).value(0);

auto x = coek::variable("x");
model.add(x);

auto xx = coek::variable("xx", A);
model.add(xx);

auto xxx = coek::variable("xxx", A*B);
model.add(xxx);

auto o = coek::objective("o").expr(p * x);
model.add(o);

auto c = coek::constraint("c").expr(x == 0);
model.add(c);

auto cc = coek::constraint("cc", Forall(i).In(A)).expr(pp(i) * xx(i) == 0);
model.add(cc);

auto ccc = coek::constraint("ccc", Forall(i).In(A).Forall(j).In(B)).expr(ppp(i, j) * xxx(i, j) == 0);
model.add(ccc);

return model;
}
"""
    )

def test_simple1():
    model = models.simple1()

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["x", "y", "o", "c1", "c2", "c3"]

    # print(generate(model=model))
    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_simple1(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("simple1");

auto x = coek::variable("x").lower(0.0).upper(1.0);
model.add(x);

auto y = coek::variable("y").lower(0.0).upper(1.0);
model.add(y);

auto o = coek::objective("o").expr(x + y);
model.add(o);

auto c1 = coek::constraint("c1").expr(x + y == 1);
model.add(c1);

auto c2 = coek::constraint("c2").expr((2 * x) + y <= 1);
model.add(c2);

auto c3 = coek::constraint("c3").expr(y - (2 * x) >= 1);
model.add(c3);

return model;
}
"""
    )


def test_hs060():
    model = models.hs060()

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["N", "x", "o", "c"]

    # print(generate(model=model))
    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_hs060(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("hs060");

auto N = coek::RangeSet(1, 4+1);

auto x = coek::variable("x", N).lower(-10).upper(10).value(2.0);
model.add(x);

auto o = coek::objective("o").expr((coek::pow(x(1) - 1, 2) + coek::pow(x(1) - x(2), 2)) + coek::pow(x(2) - x(3), 4));
model.add(o);

auto c = coek::constraint("c").expr((x(1) * (1 + coek::pow(x(2), 2))) + coek::pow(x(3), 4) == 4 + (3 * coek::sqrt(2)));
model.add(c);

return model;
}
"""
    )


def test_knapsack1():
    model = models.knapsack1(1)

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["i", "INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model))
    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_knapsack1(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("knapsack1");

auto i = coek::set_element("i");

auto INDEX = coek::RangeSet(0, 9);

auto w = coek::parameter("w", INDEX).value(1.0);

auto v = coek::parameter("v", INDEX).value(1);

auto x = coek::variable("x", INDEX).lower(0.0).upper(1.0);
model.add(x);

auto o = coek::objective("o").expr(coek::Sum(v(i) * x(i), coek::Forall(i).In(INDEX)));
model.add(o);

auto c = coek::constraint("c").expr(coek::Sum(w(i) * x(i), coek::Forall(i).In(INDEX)) <= 1.0);
model.add(c);

return model;
}
"""
    )


def test_knapsack2():
    model = models.knapsack2(1)

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["N", "i", "INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model))
    assert (
        generate(model=model)
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_knapsack2(const coek::DataPortal& )
{
coek::CompactModel model;
model.name("knapsack2");

auto N = coek::parameter("N").value(1);

auto i = coek::set_element("i");

auto INDEX = coek::RangeSet(0, (N * 10) - 1);

auto w = coek::parameter("w", INDEX).value(1 / ((N * 10) / 10.0));

auto v = coek::parameter("v", INDEX).value(1);

auto x = coek::variable("x", INDEX).lower(0.0).upper(1.0);
model.add(x);

auto o = coek::objective("o").expr(coek::Sum(v(i) * x(i), coek::Forall(i).In(INDEX)));
model.add(o);

auto c = coek::constraint("c").expr(coek::Sum(w(i) * x(i), coek::Forall(i).In(INDEX)) <= (N * 10) / 10.0);
model.add(c);

return model;
}
"""
    )


def test_knapsack3():
    model = models.knapsack3()

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["N", "i", "INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model, data={"N": "int"}))
    assert (
        generate(model=model, data={"N": "int"})
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_knapsack3(const coek::DataPortal& data)
{
coek::CompactModel model;
model.name("knapsack3");

auto N = coek::parameter("N");
if (data.contains("N")) {
    int N_value;
    data.get("N", N_value);
    N.value(N_value);
}

auto i = coek::set_element("i");

auto INDEX = coek::RangeSet(0, (N * 10) - 1);

auto w = coek::parameter("w", INDEX).value(1 / ((N * 10) / 10.0));

auto v = coek::parameter("v", INDEX).value(1);

auto x = coek::variable("x", INDEX).lower(0.0).upper(1.0);
model.add(x);

auto o = coek::objective("o").expr(coek::Sum(v(i) * x(i), coek::Forall(i).In(INDEX)));
model.add(o);

auto c = coek::constraint("c").expr(coek::Sum(w(i) * x(i), coek::Forall(i).In(INDEX)) <= (N * 10) / 10.0);
model.add(c);

return model;
}
"""
    )


def test_knapsack4():
    model = models.knapsack4()

    # order = smk.valid_order(smk.collect_info(model))
    # assert order == ["N", "i", "INDEX", "w", "v", "x", "o", "c"]

    print(generate(model=model, data={"N": "int"}))
    assert (
        generate(model=model, data={"capacity": "double", "weight":"std::map<int,double>", "value":"std::map<int,double>", "ITEMS":"std::set<int>"})
        == """
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

coek::CompactModel generate_knapsack4(const coek::DataPortal& data)
{
coek::CompactModel model;
model.name("knapsack4");

coek::ConcreteSet ITEMS;
if (data.contains("ITEMS")) {
    std::set<int> ITEMS_value;
    data.get("ITEMS", ITEMS_value);
    ITEMS = coek::SetOf(ITEMS_value);
}

auto i = coek::set_element("i");

auto value = coek::parameter("value", ITEMS);
if (data.contains("value")) {
    std::map<int,double> value_value;
    data.get("value", value_value);
    value.value(value_value);
}

auto weight = coek::parameter("weight", ITEMS);
if (data.contains("weight")) {
    std::map<int,double> weight_value;
    data.get("weight", weight_value);
    weight.value(weight_value);
}

auto capacity = coek::parameter("capacity");
if (data.contains("capacity")) {
    double capacity_value;
    data.get("capacity", capacity_value);
    capacity.value(capacity_value);
}

auto x = coek::variable("x", ITEMS).lower(0.0).upper(1.0);
model.add(x);

auto o = coek::objective("o").expr(coek::Sum(value(i) * x(i), coek::Forall(i).In(ITEMS)));
model.add(o);

auto c = coek::constraint("c").expr(coek::Sum(weight(i) * x(i), coek::Forall(i).In(ITEMS)) <= capacity);
model.add(c);

return model;
}
"""
    )
