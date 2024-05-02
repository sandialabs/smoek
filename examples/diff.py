import smoek.core as smk
from smoek.core.symbolic_diff import ReverseSDWalker


i = smk.index('i')
I = smk.set('I')
x = smk.variable(name='x').forall(i, In=I)
y = smk.variable(name='y').forall(i, In=I)
e = x[i]*y[i] + smk.sin(x[i])
walker = ReverseSDWalker()
ders = walker.walk(e)
for k, v in ders.items():
    print(f'{str(k):<30}: {str(v):<30}')
