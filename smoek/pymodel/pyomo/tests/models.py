#
# Test models
#
import smoek as smk


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
    N = smk.sequence(start=1, stop=4)
    x = smk.variable("x").index(N).value(2.0).bounds(-10, 10)

    o = smk.objective("o").expr(
        (x[1] - 1) ** 2 + (x[1] - x[2]) ** 2 + (x[2] - x[3]) ** 4
    )
    c = smk.constraint("c").expr(
        x[1] * (1 + x[2] ** 2) + x[3] ** 4 == 4 + 3 * smk.sqrt(2)
    )

    return smk.model(objective=o, constraints=[c], variables=[x], name="hs060")


def knapsack1(N):
    N = N * 1000
    W = N / 10.0

    i = smk.index("i")

    INDEX = smk.range("INDEX", stop=N)  # 0..N-1

    w = smk.parameter().name("w").forall(i, In=INDEX).value(1 / W)

    v = smk.parameter("v").forall(i, In=INDEX).value(1)

    x = smk.variable().name("x").forall(i, In=INDEX).bounds(0.0, 1.0)

    o = (
        smk.objective()
        .name("o")
        .expr(smk.sum(v[i] * x[i]).forall(i, In=INDEX))
        .minimize()
    )

    c = smk.constraint("c").expr(smk.sum(w[i] * x[i]).forall(i, In=INDEX) <= W)

    return smk.model(objective=o, constraints=[c], variables=[x], name="knapsack")


def knapsack2(N):
    N_ = smk.parameter("N").value(N)
    return knapsack1(N_)
