#
# Test models
#
import smoek as smk


def small1():
    @smk.model
    class small1:

        x = smk.variable().value(1.0)
        y = smk.variable().value(1.0)

        o = smk.objective().minimize(x**2)
        c = smk.constraint().expr(y**2 == 4)

    return small1()


def small2():
    @smk.model
    class small2:
        x = smk.variable().value(1.0)
        y = smk.variable().value(1.0)

        o = smk.objective().minimize(x)
        c = smk.constraint().expr(y**2 == 4)

    return small2()


def small3():
    @smk.model
    class small3:
        x = smk.variable().value(1.0)
        y = smk.variable().value(1.0)

        o = smk.objective().minimize(-(x * y))
        c = smk.constraint().expr(y**2 == 4)

    return small3()


def small4():
    @smk.model
    class small4:
        x = smk.variable().value(1.0)
        y = smk.variable().value(1.0)

        o = smk.objective().minimize(y**2)
        c = smk.constraint().expr(y * x == 4)

    return small4()


def small5():
    @smk.model
    class small5:
        x = smk.variable().lower(-1).upper(1).value(1.0)
        y = smk.variable().lower(-1).upper(2).value(2.0)
        v = smk.variable().lower(-1).upper(3).value(3.0)
        p = 2.0
        q = smk.parameter().value(2)

        o = smk.objective().minimize((x**2) / p + (x**2) / q)
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

    return small5()


def small6():
    @smk.model
    class small6:
        x = smk.variable().lower(-1).upper(1).value(1)
        y = smk.variable().lower(-1).upper(2).value(2)
        v = smk.variable().lower(-1).upper(3).value(3)
        p = smk.variable().value(2).fixed(True)

        o = smk.objective().minimize(x)
        c = [
            smk.constraint().expr(1 / p * v * (x - y) == 2),
            smk.constraint().expr(v * 1 / p * (x - y) == 2),
            smk.constraint().expr(v * (x - y) / p == 2),
            smk.constraint().expr(v * (x / p - y / p) == 2),
            smk.constraint().expr(v * (x - y) * (1 / p) == 2),
            smk.constraint().expr(v * (x - y) == 2 * p),
        ]

    return small6()


def testing1():
    @smk.model
    class testing1:
        a = smk.variable().lower(0).upper(1).value(0).within(smk.Integers)
        b = smk.variable().lower(0).upper(1).value(0).within(smk.Binary)
        c = smk.variable().lower(0)
        d = smk.variable().upper(0)
        e = smk.variable().fix(1.0)
        q = smk.parameter().value(2)

        o = smk.objective().maximize(3 * a + q)
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

    return testing1()


def testing2():
    @smk.model
    class testing2:
        a = smk.variable().lower(0).upper(2).value(0).within(smk.Integers)
        b = smk.variable().lower(0).upper(1).value(0).within(smk.Binary)
        q = smk.parameter().value(2)
        b.fix(1.0)

        # This forces the use of a Negate term
        e = 3 * a + q + a * a * a * (-a + b + 3 * a + 3 * b) + smk.sin(-smk.cos(a))
        o = smk.objective().minimize(e)

    return testing2()


def testing3():
    @smk.model
    class testing3:
        a = smk.variable().lower(0).upper(1).value(0).within(smk.Integers)
        b = smk.variable().lower(0).upper(1).value(0).within(smk.Binary)

        e = smk.expression()
        o = smk.objective().minimize(e)
        c = smk.constraint().expr(a + b == 1)

    return testing3()


def testing4():
    @smk.model
    class testing4:
        x = smk.variable().lower(0).upper(1).value(0).within(smk.Binary)
        y = smk.variable().lower(0).upper(1).value(0).within(smk.Binary)
        z = smk.variable().lower(0).upper(1).value(0).within(smk.Binary)
        a = smk.variable().lower(0).upper(1).value(0).within(smk.Integers)
        b = smk.variable().lower(0).upper(1).value(0).within(smk.Binary)

        o = smk.objective().minimize(a + smk.cos(x) + smk.cos(y))
        c = smk.constraint().expr(b + smk.cos(y) + smk.cos(z) == 1)

    return testing4()


# Confirming logic for variables with same upper-and-lower bounds
def testing5():
    @smk.model
    class testing5:
        x = smk.variable().lower(2).upper(2)
        o = smk.objective().minimize(x)

    return testing5()


def testing6():
    @smk.model
    class testing6:
        x = smk.variable().lower(0).upper(1).value(0)
        p = smk.parameter().value(0)
        q = smk.parameter().value(2)
        o = smk.objective().minimize(-q * x * x + p)

    return testing6()


# Confirming logic for indexed components
def testing7():
    @smk.model
    class testing7:
        A = smk.range(stop=3)  # 0..3
        B = smk.range(stop=4)  # 0..4

        i = smk.index()
        j = smk.index()

        p = smk.parameter().value(0)
        pp = smk.parameter().index_set(A).value(0)
        # ppp = smk.parameter().index_set(A*B)     # TODO
        # ppp = smk.parameter().index_set(A,B)     # TODO?
        ppp = smk.parameter().index_set(A).index_set(B).value(0)

        x = smk.variable()
        xx = smk.variable().index_set(A)
        xxx = smk.variable().index_set(A).index_set(B)

        o = smk.objective().minimize(p * x)

        c = smk.constraint().expr(x == 0)
        cc = smk.constraint().expr(pp[i] * xx[i] == 0).forall(i in A)
        ccc = (
            smk.constraint()
            .expr(ppp[i, j] * xxx[i, j] == 0)
            # .forall((i,j) in A*B)        # TODO
            .forall(i in A, j in B)
        )

    return testing7()


# Confirming logic when indexed values are used
def testing8():
    @smk.model
    class testing8:
        A = smk.range(stop=3)  # 0..3
        B = smk.range(stop=4)  # 0..4

        i = smk.index()
        j = smk.index()

        ppp = smk.parameter().index_set(A).index_set(B).value(1)
        pp = smk.parameter().forall(i in A).value(smk.sum(ppp[i, j]).forall(j in B))
        p = smk.parameter().value(smk.sum(pp[i]).forall(i in A))

        x = smk.variable().value(smk.sum(pp[i]).forall(i in A))
        xx = smk.variable().forall(i in A).value(pp[i]).lower(pp[i]).upper(pp[i])
        xxx = smk.variable().index_set(A).index_set(B)

        o = smk.objective().minimize(p * x + smk.sum(xx[i]).forall(i in A))

        c = smk.constraint().expr(smk.sum(pp[i] * xx[i]).forall(i in A) == 0)
        cc = smk.constraint().expr(pp[i] * xx[i] == 0).forall(i in A)
        ccc = (
            smk.constraint()
            .expr(smk.sum(ppp[i, j] * xxx[i, j]).forall(i in A) == 0)
            .forall(j in B)
        )

    return testing8()


def simple1():
    @smk.model
    class simple1:
        x = smk.variable().bounds(0.0, 1.0)
        y = smk.variable().bounds(0.0, 1.0)

        o = smk.objective().minimize(x + y)

        c1 = smk.constraint().expr(x + y == 1)
        c2 = smk.constraint().expr(2 * x + y <= 1)
        c3 = smk.constraint().expr(y - 2 * x >= 1)

    return simple1()


def hs060():
    @smk.model
    class hs060:
        # Adapted from cute suite.
        N = smk.sequence(start=1, stop=4)
        x = smk.variable().index_set(N).value(2.0).bounds(-10, 10)

        o = smk.objective().minimize(
            (x[1] - 1) ** 2 + (x[1] - x[2]) ** 2 + (x[2] - x[3]) ** 4
        )
        c = smk.constraint().expr(
            x[1] * (1 + x[2] ** 2) + x[3] ** 4 == 4 + 3 * smk.sqrt(2)
        )

    return hs060()


def knapsack1(N=1, name="knapsack1"):

    @smk.model(name=name)
    class knapsack:
        N_ = N * 10
        capacity = N_ / 10.0

        i = smk.index()

        INDEX = smk.range(stop=N_ - 1)  # 0..N-1

        w = smk.parameter().index_set(INDEX).value(1 / capacity)

        v = smk.parameter().index_set(INDEX).value(1)

        x = smk.variable().index_set(INDEX).bounds(0.0, 1.0)

        o = smk.objective().maximize(smk.sum(v[i] * x[i]).forall(i in INDEX))

        c = smk.constraint().expr(
            smk.sum(w[i] * x[i]).forall(i in INDEX) <= capacity
        )

    return knapsack()


def knapsack2(N=1):
    N_ = smk.parameter("N").value(N)
    return knapsack1(N_, "knapsack2")


def knapsack3():
    N_ = smk.parameter("N")
    return knapsack1(N_, "knapsack3")


def knapsack4():

    @smk.model
    class knapsack4:
        ITEMS = smk.set()

        i = smk.index()

        value = smk.parameter().index_set(ITEMS)

        weight = smk.parameter().index_set(ITEMS)

        capacity = smk.parameter()

        x = smk.variable().index_set(ITEMS).bounds(0.0, 1.0)

        o = (
            smk.objective()
            .maximize(smk.sum(value[i] * x[i]).forall(i in ITEMS))
        )

        c = smk.constraint().expr(
            smk.sum(weight[i] * x[i]).forall(i in ITEMS) <= capacity
        )

    return knapsack4()


def pmedian1(N_=10, P=1):

    @smk.model
    class pmedian1:
        # N_ - Locations
        M_ = N_  # Customers
        # P_ - Facilities

        n = smk.index()
        m = smk.index()
        N = smk.range(stop=N_ - 1)  # 0..N_-1
        M = smk.range(stop=M_ - 1)  # 0..M_-1

        d = smk.parameter().forall(n in N, m in M).value(1.0 + 1.0 / (n + m + 1))

        x = (
            smk.variable()
            .index_set(N)
            .index_set(M)
            .bounds(0.0, 1.0)
            .value(0.0)
            .within(smk.Binary)
        )
        y = smk.variable().index_set(N).bounds(0.0, 1.0).value(0.0).within(smk.Binary)

        o = smk.objective().minimize(smk.sum(d[n, m] * x[n, m]).forall(n in N, m in M))

        single_x = (
            smk.constraint()
            .expr(smk.sum(x[n, m]).forall(n in N) == 1)
            .forall(m in M)
        )

        bound_y = smk.constraint().expr(x[n, m] - y[n] <= 0).forall(n in N, m in M)

        # num_facilities
        num_facilities = smk.constraint().expr(smk.sum(y[n]).forall(n in N) == P)

    return pmedian1()


def pmedian2(N_=10, P=1):

    @smk.model
    class pmedian2:
        # N_ - Locations
        M_ = N_  # Customers
        # P_ - Facilities

        n = smk.index()
        m = smk.index()
        N = smk.range(stop=N_ - 1)  # 0..N_-1
        M = smk.range(stop=M_ - 1)  # 0..M_-1

        d = smk.data().forall(n in N, m in M).value(1.0 + 1.0 / (n + m + 1))

        x = (
            smk.variable()
            .index_set(N)
            .index_set(M)
            .bounds(0.0, 1.0)
            .value(0.0)
            .within(smk.Binary)
        )
        y = smk.variable().index_set(N).bounds(0.0, 1.0).value(0.0).within(smk.Binary)

        o = smk.objective().minimize(smk.sum(d[n, m] * x[n, m]).forall(n in N, m in M))

        single_x = (
            smk.constraint()
            .expr(smk.sum(x[n, m]).forall(n in N) == 1)
            .forall(m in M)
        )

        bound_y = smk.constraint().expr(x[n, m] - y[n] <= 0).forall(n in N, m in M)

        num_facilities = smk.constraint().expr(smk.sum(y[n]).forall(n in N) == P)

    return pmedian2()


# Adapted from StochasticPrograms.jl documentation
#   https://martinbiel.github.io/StochasticPrograms.jl/dev/manual/quickstart/#Quick-start
# Taken from Introduction to Stochastic Programing.
#   https://link.springer.com/book/10.1007/978-1-4614-0237-4
def sp1():
    @smk.stochastic_model
    class sp1:

        @smk.model
        class stage1:
            x1 = smk.variable().lower(40)
            x2 = smk.variable().lower(40)

            o = smk.objective().minimize(100 * x1 + 150 * x2)
            c = smk.constraint().expr(x1 + x2 <= 120)

        @smk.model
        class stage2:

            q1 = smk.uncertain()
            q2 = smk.uncertain()
            q3 = smk.uncertain()
            d1 = smk.uncertain()
            d2 = smk.uncertain()

            y1 = smk.variable().bounds(0, d1)
            y2 = smk.variable().bounds(0, d2)

            o = smk.objective().minimize(q1 * y1 + q2 * y2)

            c0 = smk.constraints().expr(6 * y1 + 10 * y2 <= 60 * x1)
            c1 = smk.constraints().expr(8 * y1 + 5 * y2 <= 80 * x2)

    return sp1()
