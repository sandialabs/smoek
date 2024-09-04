#
# Test models
#
import smoek as smk


def small1():
    x = smk.variable("x").value(1.0)
    y = smk.variable("y").value(1.0)

    o = smk.objective("o").expr(x**2)
    c = smk.constraint("c").expr(y**2 == 4)
    return smk.model(objective=o, constraints=[c], variables=[x, y], name="small1")


def small2():
    x = smk.variable("x").value(1.0)
    y = smk.variable("y").value(1.0)

    o = smk.objective("o").expr(x)
    c = smk.constraint("c").expr(y**2 == 4)
    return smk.model(objective=o, constraints=[c], variables=[x, y], name="small2")


def small3():
    x = smk.variable("x").value(1.0)
    y = smk.variable("y").value(1.0)

    o = smk.objective("o").expr(x * y)
    c = smk.constraint("c").expr(y**2 == 4)
    return smk.model(objective=o, constraints=[c], variables=[x, y], name="small3")


def small4():
    x = smk.variable("x").value(1.0)
    y = smk.variable("y").value(1.0)

    o = smk.objective("o").expr(y**2)
    c = smk.constraint("c").expr(y * x == 4)
    return smk.model(objective=o, constraints=[c], variables=[x, y], name="small4")


def small5():
    x = smk.variable("x").lower(-1).upper(1).value(1.0)
    y = smk.variable("y").lower(-1).upper(2).value(2.0)
    v = smk.variable("v").lower(-1).upper(3).value(3.0)
    p = 2.0
    q = smk.parameter("q").value(2)

    o = smk.objective().expr((x**2) / p + (x**2) / q)
    c = [
        smk.constraint().expr(1 / p * v * (x - y) == 2),
        smk.constraint().expr(v * 1 / p * (x - y) == 2),
        smk.constraint().expr(v * (x - y) / p == 2),
        smk.constraint().expr(v * (x / p - y / p) == 2),
        smk.constraint().expr(v * (x - y) * (1 / p) == 2),
        smk.constraint().expr(v * (x - y) == 2 * p),
        smk.constraint().expr(1 / q * v * (x - y) == 2),
        smk.constraint().expr(v * 1 / q * (x - y) == 2),
        smk.constraint().expr(v * (x - y) / q == 2),
        smk.constraint().expr(v * (x / p - y / q) == 2),
        smk.constraint().expr(v * (x - y) * (1 / q) == 2),
        smk.constraint().expr(v * (x - y) == 2 * q),
    ]
    return smk.model(objective=o, constraints=c, variables=[x, y, v], name="small5")


def small6():
    x = smk.variable().lower(-1).upper(1).value(1)
    y = smk.variable().lower(-1).upper(2).value(2)
    v = smk.variable().lower(-1).upper(3).value(3)
    p = smk.variable()
    p.value(2)
    p.fixed(True)

    o = smk.objective().expr(x)
    c = [
        smk.constraint().expr(1 / p * v * (x - y) == 2),
        smk.constraint().expr(v * 1 / p * (x - y) == 2),
        smk.constraint().expr(v * (x - y) / p == 2),
        smk.constraint().expr(v * (x / p - y / p) == 2),
        smk.constraint().expr(v * (x - y) * (1 / p) == 2),
        smk.constraint().expr(v * (x - y) == 2 * p),
    ]
    return smk.model(objective=o, constraints=c, variables=[x, y, v, p], name="small6")


def testing1():
    a = smk.variable("a").lower(0).upper(1).value(0).within(smk.Integers)
    b = smk.variable("b").lower(0).upper(1).value(0).within(smk.Binary)
    c = smk.variable().lower(0)
    d = smk.variable().upper(0)
    e = smk.variable("e")
    q = smk.parameter("q").value(2)

    o = smk.objective().expr(3 * a + q).sense(smk.maximize)
    C = [
        smk.constraint().expr(3 * b + q - a <= 0),
        smk.constraint().expr(3 * b + b == 0),
        smk.constraint().expr(3 * b * a + q + b * b + b * b == 0),
        smk.constraint().expr(3 * b * b + q - a * b - a * a <= 0),
        smk.constraint().expr(smk.inequality(-7, 3 * b * b + q - a * b - a * a, 7)),
        smk.constraint().expr(c + d == 0),
        smk.constraint().expr(e + 3 * d == 1),
        smk.constraint().expr(smk.inequality(7, 3 * b + q - a, 7)),
    ]
    e.fix(1.0)
    return smk.model(
        objective=o, constraints=C, variables=[a, b, c, d, e, q], name="testing1"
    )


def testing2():
    a = smk.variable("a").lower(0).upper(1).value(0).within(smk.Integers)
    b = smk.variable("b").lower(0).upper(1).value(0).within(smk.Binary)
    q = smk.parameter("q").value(2)
    b.fix(2.0)

    # This forces the use of a Negate term
    e = 3 * a + q + a * a * a * (-a + b + 3 * a + 3 * b) + smk.sin(-smk.cos(a))
    o = smk.objective().expr(e)
    return smk.model(
        objective=o, constraints=[], variables=[a, b, q, b], name="testing2"
    )


def testing3():
    a = smk.variable("a").lower(0).upper(1).value(0).within(smk.Integers)
    b = smk.variable("b").lower(0).upper(1).value(0).within(smk.Binary)

    e = smk.expression()
    o = smk.objective().expr(e)
    c = smk.constraint().expr(a + b == 1)
    return smk.model(objective=o, constraints=[c], variables=[a, b], name="testing3")


def testing4():
    x = smk.variable("x").lower(0).upper(1).value(0).within(smk.Binary)
    y = smk.variable("y").lower(0).upper(1).value(0).within(smk.Binary)
    z = smk.variable("z").lower(0).upper(1).value(0).within(smk.Binary)
    a = smk.variable("a").lower(0).upper(1).value(0).within(smk.Integers)
    b = smk.variable("b").lower(0).upper(1).value(0).within(smk.Binary)

    o = smk.objective().expr(a + smk.cos(x) + smk.cos(y))
    c = smk.constraint().expr(b + smk.cos(y) + smk.cos(z) == 1)
    return smk.model(
        objective=o, constraints=[c], variables=[x, y, z, a, b], name="testing4"
    )


# Confirming logic for variables with same upper-and-lower bounds
def testing5():
    x = smk.variable("x").lower(2).upper(2)
    o = smk.objective("o").expr(x)
    return smk.model(objective=o, constraints=[], variables=[x], name="testing5")


def testing6():
    x = smk.variable("x").lower(0).upper(1).value(0)
    p = smk.parameter("p").value(0)
    q = smk.parameter("q").value(2)
    o = smk.objective("o").expr(-q * x * x + p)
    return smk.model(objective=o, constraints=[], variables=[x], name="testing6")


# Confirming logic for indexed components
def testing7():
    A = smk.range("A", stop=10)  # 0..9
    B = smk.range("B", stop=11)  # 0..9

    i = smk.index("i")
    j = smk.index("j")

    p = smk.parameter("p").value(0)
    pp = smk.parameter("pp").index_set(A).value(0)
    # ppp = smk.parameter("ppp").index_set(A*B)     # TODO
    # ppp = smk.parameter("ppp").index_set(A,B)     # TODO?
    ppp = smk.parameter("ppp").index_set(A).index_set(B).value(0)

    x = smk.variable("x")
    xx = smk.variable("xx").index_set(A)
    xxx = smk.variable("xxx").index_set(A).index_set(B)

    o = smk.objective("o").expr(p * x)

    c = smk.constraint("c").expr(x == 0)
    cc = smk.constraint("cc").expr(pp[i] * xx[i] == 0).forall(i, In=A)
    ccc = (
        smk.constraint("ccc")
        .expr(ppp[i, j] * xxx[i, j] == 0)
        # .forall((i,j), In=A*B)        # TODO
        # .forall(i, j, In=A*B)         # TODO?
        .forall(i, In=A)
        .forall(j, In=B)
    )

    return smk.model(
        objective=o, constraints=[c, cc, ccc], variables=[x, xx, xxx], name="testing7"
    )


def simple1():
    x = smk.variable("x").bounds(0.0, 1.0)
    y = smk.variable().name("y").bounds(0.0, 1.0)

    o = smk.objective().name("o").expr(x + y).minimize()

    c1 = smk.constraint("c1").expr(x + y == 1)
    c2 = smk.constraint("c2").expr(2 * x + y <= 1)
    c3 = smk.constraint("c3").expr(y - 2 * x >= 1)

    return smk.model(
        objective=o, constraints=[c1, c2, c3], variables=[x, y], name="simple1"
    )


def hs060():
    # Adapted from cute suite.
    N = smk.sequence("N", start=1, stop=4)
    x = smk.variable("x").index_set(N).value(2.0).bounds(-10, 10)

    o = smk.objective("o").expr(
        (x[1] - 1) ** 2 + (x[1] - x[2]) ** 2 + (x[2] - x[3]) ** 4
    )
    c = smk.constraint("c").expr(
        x[1] * (1 + x[2] ** 2) + x[3] ** 4 == 4 + 3 * smk.sqrt(2)
    )

    return smk.model(objective=o, constraints=[c], variables=[x], name="hs060")


def knapsack1(N=1, name="knapsack1"):
    N_ = N * 10
    capacity = N_ / 10.0

    i = smk.index("i")

    INDEX = smk.range("INDEX", stop=N_)  # 0..N-1

    w = smk.parameter().name("w").index_set(INDEX).value(1 / capacity)

    v = smk.parameter("v").index_set(INDEX).value(1)

    x = smk.variable().name("x").index_set(INDEX).bounds(0.0, 1.0)

    o = (
        smk.objective()
        .name("o")
        .expr(smk.sum(v[i] * x[i]).forall(i, In=INDEX))
        .minimize()
    )

    c = smk.constraint("c").expr(smk.sum(w[i] * x[i]).forall(i, In=INDEX) <= capacity)

    return smk.model(objective=o, constraints=[c], variables=[x], name=name)


def knapsack2(N=1):
    N_ = smk.parameter("N").value(N)
    return knapsack1(N_, "knapsack2")


def knapsack3():
    N_ = smk.parameter("N")
    return knapsack1(N_, "knapsack3")


def knapsack4(name="knapsack4"):

    ITEMS = smk.set("ITEMS")

    i = smk.index("i")

    value = smk.parameter("value").index_set(ITEMS)

    weight = smk.parameter("weight").index_set(ITEMS)

    capacity = smk.parameter("capacity")


    x = smk.variable("x").index_set(ITEMS).bounds(0.0, 1.0)

    o = (
        smk.objective()
        .name("o")
        .expr(smk.sum(value[i] * x[i]).forall(i, In=ITEMS))
        .minimize()
    )

    c = smk.constraint("c").expr(smk.sum(weight[i] * x[i]).forall(i, In=ITEMS) <= capacity)

    return smk.model(objective=o, constraints=[c], variables=[x], name=name)

