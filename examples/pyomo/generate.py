import os
import smoek as smk
import smoek.core.tests.models as models
from smoek.code.pyomo import generate

if not os.path.exists("models"):
    os.mkdir("models")

testnames = ["small1", "small2", "small3", "small4", "small5", "small6",
                "testing1", "testing2", "testing4", "testing5", "testing6", "testing7",
                "simple1", "hs060",
                "knapsack1", "knapsack2", "knapsack3", "knapsack4"
]

data = {
    "knapsack3": {"N"},
    "knapsack4": {"value", "weight", "capacity", "ITEMS"},
}

for name in testnames:
    print("GENERATING "+name)
    model = getattr(models, name)()
    data_option = data.get(name,{}) 
    generate(model=model, outfile=f"models/{name}.py", data=data_option)

