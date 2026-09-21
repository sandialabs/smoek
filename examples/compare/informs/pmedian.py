import smoek as smk


@smk.model
class pmedian:

    dp = smk.DataPortal()
    M = N = 100
    P = 1

    n = smk.index("n")
    m = smk.index("m")
    N = smk.range("N", stop=N - 1)  # 0..N-1
    M = smk.range("M", stop=M - 1)  # 0..M-1

    d = smk.parameter("d").forall(n, In=N).forall(m, In=M).value(dp["d"])

    x = smk.variable("x").index_set(N).index_set(M).bounds(0.0, 1.0).value(0.0).within(smk.Binary)
    y = smk.variable("y").index_set(N).bounds(0.0, 1.0).value(0.0).within(smk.Binary)

    o = smk.objective().minimize(smk.sum(d[n, m] * x[n, m]).forall(n, In=N).forall(m, In=M))

    c1 = smk.constraint("single_x").expr(smk.sum(x[n, m]).forall(n, In=N) == 1).forall(m, In=M)

    c2 = smk.constraint("bound_y").expr(x[n, m] - y[n] <= 0).forall(n, In=N).forall(m, In=M)

    c3 = smk.constraint("num_facilities").expr(smk.sum(y[n]).forall(n, In=N) == P)


from smoek.io.tex import LatexWriter

writer = LatexWriter()
writer.write_model(pmedian(), "pmedian.tex")
