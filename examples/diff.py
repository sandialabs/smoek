import smoek as smk
from smoek.diff.symbolic_diff import ReverseSDWalker

i = smk.index("i")
I = smk.index_set("I")
x = smk.variable(name="x").forall(i, In=I)
y = smk.variable(name="y").forall(i, In=I)
e = x[i] * y[i] + smk.sin(x[i])
walker = ReverseSDWalker()
ders = walker.walk(e)
for k, v in ders.items():
    print(f"{str(k):<30}: {str(v):<30}")
