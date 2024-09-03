import smoek as smk
import smoek.core.tests.models as models
from smoek.code.pyomo import generate

model = models.small1()
generate(model=model, outfile="small1.py")

model = models.small2()
generate(model=model, outfile="small2.py")

model = models.small3()
generate(model=model, outfile="small3.py")

model = models.small4()
generate(model=model, outfile="small4.py")

model = models.small5()
generate(model=model, outfile="small5.py")

model = models.small6()
generate(model=model, outfile="small6.py")

model = models.testing1()
generate(model=model, outfile="testing1.py")

model = models.testing2()
generate(model=model, outfile="testing2.py")

#model = models.testing3()
#generate(model=model, outfile="testing3.py")

model = models.testing4()
generate(model=model, outfile="testing4.py")

model = models.testing5()
generate(model=model, outfile="testing5.py")

model = models.testing6()
generate(model=model, outfile="testing6.py")

model = models.testing7()
generate(model=model, outfile="testing7.py")

model = models.simple1()
generate(model=model, outfile="simple1.py")

model = models.hs060()
generate(model=model, outfile="hs060.py")

model = models.knapsack1(1)
generate(model=model, outfile="knapsack1.py")

model = models.knapsack2(1)
generate(model=model, outfile="knapsack2.py")

model = models.knapsack3()
generate(model=model, outfile="knapsack3.py", data={"N"})

model = models.knapsack4()
generate(model=model, outfile="knapsack4.py", data={"value", "weight", "max_weight", "ITEMS"})

