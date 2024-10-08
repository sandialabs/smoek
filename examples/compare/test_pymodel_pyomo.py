import pyomo
from pyomo.common.timing import tic,toc
from models import pmedian1, pmedian2
from smoek.pymodel.pyomo import generate

sizes = [100]
suffixes = ['lp', 'nl']
tests = {'pmedian1':pmedian1, 'pmedian2':pmedian2}
ntrials = 1

def run(test, size, trial, suffix):
    print("-"*70)
    tic(f"Test: {test} {size} {trial} {suffix}")

    smoek_model = tests[test](size)
    toc("Smoek model generated")

    jsonfile = f"data/{test}_{size}.json"
    if os.path.exists(jsonfile):
        data = smk.load_data_from_json(filename=jsonfile)
    else:
        data = {}
    toc("Load JSON data")

    pyomo_model = generate(model=smoek_model, data=data)
    toc("Pyomo model generated")

    fname = f"{suffix}files/pymodel_pyomo_{test}_{size}_{trial}.{suffix}"
    pyomo_model.write(fname)
    toc(f"Writing file {fname}")

for test in tests:
    for size in sizes:
        for trial in range(ntrials):
            for suffix in suffixes:
                run(test, size, trial, suffix)

        

