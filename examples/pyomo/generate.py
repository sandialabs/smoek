import os
import smoek as smk
import smoek.core.tests.models as models
from smoek.code.pyomo import generate

if not os.path.exists("models"):
    os.mkdir("models")

model = models.small1()
generate(model=model, outfile="models/small1.py")

model = models.small2()
generate(model=model, outfile="models/small2.py")

model = models.small3()
generate(model=model, outfile="models/small3.py")

model = models.small4()
generate(model=model, outfile="models/small4.py")

model = models.small5()
generate(model=model, outfile="models/small5.py")

model = models.small6()
generate(model=model, outfile="models/small6.py")

model = models.testing1()
generate(model=model, outfile="models/testing1.py")

model = models.testing2()
generate(model=model, outfile="models/testing2.py")

#model = models.testing3()
#generate(model=model, outfile="models/testing3.py")

model = models.testing4()
generate(model=model, outfile="models/testing4.py")

model = models.testing5()
generate(model=model, outfile="models/testing5.py")

model = models.testing6()
generate(model=model, outfile="models/testing6.py")

model = models.testing7()
generate(model=model, outfile="models/testing7.py")

model = models.simple1()
generate(model=model, outfile="models/simple1.py")

model = models.hs060()
generate(model=model, outfile="models/hs060.py")

model = models.knapsack1(1)
generate(model=model, outfile="models/knapsack1.py")

model = models.knapsack2(1)
generate(model=model, outfile="models/knapsack2.py")

model = models.knapsack3()
generate(model=model, outfile="models/knapsack3.py", data={"N"})

model = models.knapsack4()
generate(model=model, outfile="models/knapsack4.py", data={"value", "weight", "max_weight", "ITEMS"})

