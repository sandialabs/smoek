import smoek as smk
import smoek.core.tests.models as models
from smoek.code.coek import generate

model = models.simple1()
generate(model=model, outfile="simple1.cpp")

model = models.knapsack1(10)
generate(model=model, outfile="knapsack1.cpp")

model = models.knapsack2(10)
generate(model=model, outfile="knapsack2.cpp")

model = models.knapsack3()
generate(model=model, outfile="knapsack3.cpp", data={"N":"int"})

