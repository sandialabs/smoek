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


