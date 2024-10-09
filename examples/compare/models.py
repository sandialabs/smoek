#
# Test models
#
import smoek as smk


def knapsack1(N=1, name="knapsack1"):
    N_ = N * 10
    capacity = N_ / 10.0

    i = smk.index("i")

    INDEX = smk.range("INDEX", stop=N_ - 1)  # 0..N-1

    w = smk.parameter().name("w").index_set(INDEX).value(1 / capacity)

    v = smk.parameter("v").index_set(INDEX).value(1)

    x = smk.variable().name("x").index_set(INDEX).bounds(0.0, 1.0)

    o = (
        smk.objective()
        .name("o")
        .expr(smk.sum(v[i] * x[i]).forall(i, In=INDEX))
        .maximize()
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
        .maximize()
    )

    c = smk.constraint("c").expr(
        smk.sum(weight[i] * x[i]).forall(i, In=ITEMS) <= capacity
    )

    return smk.model(objective=o, constraints=[c], variables=[x], name=name)


def pmedian1(N_=10, P=1, data=None):

    # N_ - Locations
    M_ = N_  # Customers
    # P_ - Facilities

    n = smk.index("n")
    m = smk.index("m")
    N = smk.range("N", stop=N_ - 1)  # 0..N_-1
    M = smk.range("M", stop=M_ - 1)  # 0..M_-1

    d = (
        smk.parameter("d")
        .forall(n, In=N)
        .forall(m, In=M)
        .value(1.0 + 1.0 / (n + m + 1))
    )

    x = (
        smk.variable("x")
        .index_set(N)
        .index_set(M)
        .bounds(0.0, 1.0)
        .value(0.0)
        .within(smk.Binary)
    )
    y = smk.variable("y").index_set(N).bounds(0.0, 1.0).value(0.0).within(smk.Binary)

    # obj
    o = smk.objective().expr(smk.sum(d[n, m] * x[n, m]).forall(n, In=N).forall(m, In=M))

    # single_x
    c1 = (
        smk.constraint("single_x")
        .expr(smk.sum(x[n, m]).forall(n, In=N) == 1)
        .forall(m, In=M)
    )

    # bound_y
    c2 = (
        smk.constraint("bound_y")
        .expr(x[n, m] - y[n] <= 0)
        .forall(n, In=N)
        .forall(m, In=M)
    )

    # num_facilities
    c3 = smk.constraint("num_facilities").expr(smk.sum(y[n]).forall(n, In=N) == P)

    return smk.model(
        objective=o, constraints=[c1, c2, c3], variables=[x, y], name="pmedian1"
    )

def pmedian2(N_=10, P=1, data=None):

    # N_ - Locations
    M_ = N_  # Customers
    # P_ - Facilities

    n = smk.index("n")
    m = smk.index("m")
    N = smk.range("N", stop=N_ - 1)  # 0..N_-1
    M = smk.range("M", stop=M_ - 1)  # 0..M_-1

    d = (
        smk.data("d")
        .forall(n, In=N)
        .forall(m, In=M)
        .value(1.0 + 1.0 / (n + m + 1))
    )

    x = (
        smk.variable("x")
        .index_set(N)
        .index_set(M)
        .bounds(0.0, 1.0)
        .value(0.0)
        .within(smk.Binary)
    )
    y = smk.variable("y").index_set(N).bounds(0.0, 1.0).value(0.0).within(smk.Binary)

    # obj
    o = smk.objective().expr(smk.sum(d[n, m] * x[n, m]).forall(n, In=N).forall(m, In=M))

    # single_x
    c1 = (
        smk.constraint("single_x")
        .expr(smk.sum(x[n, m]).forall(n, In=N) == 1)
        .forall(m, In=M)
    )

    # bound_y
    c2 = (
        smk.constraint("bound_y")
        .expr(x[n, m] - y[n] <= 0)
        .forall(n, In=N)
        .forall(m, In=M)
    )

    # num_facilities
    c3 = smk.constraint("num_facilities").expr(smk.sum(y[n]).forall(n, In=N) == P)

    return smk.model(
        objective=o, constraints=[c1, c2, c3], variables=[x, y], name="pmedian2"
    )


def pmedian3(N_=10, P=1, data=None):

    # N_ - Locations
    M_ = N_  # Customers
    # P_ - Facilities

    n = smk.index("n")
    m = smk.index("m")
    N = smk.range("N", stop=N_ - 1)  # 0..N_-1
    M = smk.range("M", stop=M_ - 1)  # 0..M_-1

    d = (
        smk.parameter("d")
        .forall(n, In=N)
        .forall(m, In=M)
        .value(data['d'])
    )

    x = (
        smk.variable("x")
        .index_set(N)
        .index_set(M)
        .bounds(0.0, 1.0)
        .value(0.0)
        .within(smk.Binary)
    )
    y = smk.variable("y").index_set(N).bounds(0.0, 1.0).value(0.0).within(smk.Binary)

    # obj
    o = smk.objective().expr(smk.sum(d[n, m] * x[n, m]).forall(n, In=N).forall(m, In=M))

    # single_x
    c1 = (
        smk.constraint("single_x")
        .expr(smk.sum(x[n, m]).forall(n, In=N) == 1)
        .forall(m, In=M)
    )

    # bound_y
    c2 = (
        smk.constraint("bound_y")
        .expr(x[n, m] - y[n] <= 0)
        .forall(n, In=N)
        .forall(m, In=M)
    )

    # num_facilities
    c3 = smk.constraint("num_facilities").expr(smk.sum(y[n]).forall(n, In=N) == P)

    return smk.model(
        objective=o, constraints=[c1, c2, c3], variables=[x, y], name="pmedian3"
    )

def pmedian4(N_=10, P=1, data=None):

    # N_ - Locations
    M_ = N_  # Customers
    # P_ - Facilities

    n = smk.index("n")
    m = smk.index("m")
    N = smk.range("N", stop=N_ - 1)  # 0..N_-1
    M = smk.range("M", stop=M_ - 1)  # 0..M_-1

    d = (
        smk.data("d")
        .forall(n, In=N)
        .forall(m, In=M)
        .value(data['d'])
    )

    x = (
        smk.variable("x")
        .index_set(N)
        .index_set(M)
        .bounds(0.0, 1.0)
        .value(0.0)
        .within(smk.Binary)
    )
    y = smk.variable("y").index_set(N).bounds(0.0, 1.0).value(0.0).within(smk.Binary)

    # obj
    o = smk.objective().expr(smk.sum(d[n, m] * x[n, m]).forall(n, In=N).forall(m, In=M))

    # single_x
    c1 = (
        smk.constraint("single_x")
        .expr(smk.sum(x[n, m]).forall(n, In=N) == 1)
        .forall(m, In=M)
    )

    # bound_y
    c2 = (
        smk.constraint("bound_y")
        .expr(x[n, m] - y[n] <= 0)
        .forall(n, In=N)
        .forall(m, In=M)
    )

    # num_facilities
    c3 = smk.constraint("num_facilities").expr(smk.sum(y[n]).forall(n, In=N) == P)

    return smk.model(
        objective=o, constraints=[c1, c2, c3], variables=[x, y], name="pmedian4"
    )

