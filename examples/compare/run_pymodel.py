import sys
import os
import pyomo
from pyomo.common.gc_manager import PauseGC
from pyomo.common.timing import tic, toc
from smoek_models import pmedian1, pmedian2, pmedian3, pmedian4
from smoek.pymodel.pyomo import generate as generate_pyomo
from smoek.pymodel.poek import generate as generate_poek
from smoek import JsonDataPortal

tests = {"pmedian1": pmedian1, "pmedian3": pmedian3}


def run_pyomo(test, size, trial, suffix):
    print("-" * 70)
    tic(f"Test: pyomo {test} {size} {trial} {suffix}")

    jsonfile = f"data/{test}_{size}.json"
    if os.path.exists(jsonfile):
        data = JsonDataPortal(filename=jsonfile)
    else:
        data = {}
    toc(f"Create JSON data portal")

    smoek_model = tests[test](size, data=data)
    toc("Smoek model generated")

    pyomo_model = generate_pyomo(model=smoek_model, data=data)
    toc("Pyomo model generated")

    fname = f"{suffix}files/pymodel_pyomo_{test}_{size}_{trial}.{suffix}"
    pyomo_model.write(fname)
    toc(f"Writing file {fname}")


def run_poek1(test, size, trial, suffix):
    print("-" * 70)
    tic(f"Test: poek1 {test} {size} {trial} {suffix}")

    jsonfile = f"data/{test}_{size}.json"
    if os.path.exists(jsonfile):
        data = JsonDataPortal(filename=jsonfile)
    else:
        data = {}
    toc(f"Create JSON data portal")

    smoek_model = tests[test](size, data=data)
    toc("Smoek model generated")

    poek_model = generate_poek(model=smoek_model, data=data)
    M = poek_model.expand()
    toc("Poek model generated")

    fname = f"{suffix}files/pymodel_poek1_{test}_{size}_{trial}.{suffix}"
    M.write(fname)
    toc(f"Writing file {fname}")


def run_poek2(test, size, trial):
    print("-" * 70)
    tic(f"Test: poek2 {test} {size} {trial} lp")

    jsonfile = f"data/{test}_{size}.json"
    if os.path.exists(jsonfile):
        data = JsonDataPortal(filename=jsonfile)
    else:
        data = {}
    toc(f"Create JSON data portal")

    smoek_model = tests[test](size, data=data)
    toc("Smoek model generated")

    poek_model = generate_poek(model=smoek_model, data=data)
    toc("Poek model generated")

    fname = f"lpfiles/pymodel_poek2_{test}_{size}_{trial}.lp"
    poek_model.write(fname)
    toc(f"Writing file {fname}")


def run(pymodel, test, size, trial, suffix):
    if pymodel == "pyomo":
        run_pyomo(test, size, trial, suffix)
    elif pymodel == "poek1":
        run_poek1(test, size, trial, suffix)
    elif pymodel == "poek2":
        if suffix == "lp":
            run_poek2(test, size, trial)
        else:
            print("-" * 70)
            print(f"WARNING: cannot run poek2 test using {suffix} suffix.")
    else:
        print("Unknown pymodel: " + pymodel)


assert len(sys.argv) == 6, "run_pymodel.py <pymodel> <test> <size> <trial> <suffix>"
pymodel = sys.argv[1]
test = sys.argv[2]
size = int(sys.argv[3])
trial = int(sys.argv[4])
suffix = sys.argv[5]

with PauseGC() as pgc:
    run(pymodel, test, size, trial, suffix)
