import smoek as smk
import smoek.core.tests.models as models
from smoek.code.pyomo import generate

model = models.simple1()
generate(model=model, outfile="simple1.py")

model = models.hs060()
generate(model=model, outfile="hs060.py")

model = models.knapsack1(1)
generate(model=model, outfile="knapsack1.py")

model = models.knapsack2(1)
generate(model=model, outfile="knapsack2.py")

model = models.knapsack3()
generate(model=model, outfile="knapsack3.py", data={"N":"int"})

