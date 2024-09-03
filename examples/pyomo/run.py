import os
import json
import sys

from small1 import generate_small1
from small2 import generate_small2
from small3 import generate_small3
from small4 import generate_small4
from small5 import generate_small5
from small6 import generate_small6
from testing1 import generate_testing1
from testing2 import generate_testing2
from testing3 import generate_testing3
from testing4 import generate_testing4
from testing5 import generate_testing5
from testing6 import generate_testing6
from testing7 import generate_testing7
from simple1 import generate_simple1
from hs060 import generate_hs060
from knapsack1 import generate_knapsack1
from knapsack2 import generate_knapsack2
from knapsack3 import generate_knapsack3

if len(sys.argv) == 1:
    print("run.py <test-name> [<json-data-filename>]")
    sys.exit(0)

if len(sys.argv) >= 2:
    testname = sys.argv[1]
if len(sys.argv) >= 3:
    jsonfile = sys.argv
    assert os.path.exists(jsonfile), "Specified JSON file does not exist: "+jsonfile
elif os.path.exists(os.path.join("data",testname+".json")):
    jsonfile = os.path.join("data",testname+".json")
else:
    jsonfile = None

if jsonfile:
    with open(jsonfile, 'r') as INPUT:
        data = json.load(INPUT)
else:
    data = {}

if testname == "small1":
    model = generate_small1(data)
elif testname == "small2":
    model = generate_small2(data)
elif testname == "small3":
    model = generate_small3(data)
elif testname == "small4":
    model = generate_small4(data)
elif testname == "small5":
    model = generate_small5(data)
elif testname == "small6":
    model = generate_small6(data)
elif testname == "testing1":
    model = generate_testing1(data)
elif testname == "testing2":
    model = generate_testing2(data)
elif testname == "testing3":
    model = generate_testing3(data)
elif testname == "testing4":
    model = generate_testing4(data)
elif testname == "testing5":
    model = generate_testing6(data)
elif testname == "testing6":
    model = generate_testing6(data)
elif testname == "testing7":
    model = generate_testing7(data)
elif testname == "simple1":
    model = generate_simple1(data)
elif testname == "hs060":
    model = generate_hs060(data)
elif testname == "knapsack1":
    model = generate_knapsack1(data)
elif testname == "knapsack2":
    model = generate_knapsack2(data)
elif testname == "knapsack3":
    model = generate_knapsack3(data)
elif testname == "knapsack4":
    model = generate_knapsack4(data)

model.pprint()
model.write(testname+".nl")

