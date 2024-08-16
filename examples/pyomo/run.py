import os
import json
import sys

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

if testname == "simple1":
    model = generate_simple1(data)
elif testname == "hs060":
    model = generate_hs060(data)
elif testname == "knapsack1":
    model = generate_knapsack1(data)
elif testname == "knapsack2":
    model = generate_knapsack2(data)
elif testname == "knapsack3":
    model = generate_knapsack3(data)

model.pprint()
model.write(testname+".nl")

