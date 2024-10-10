import sys
import os
import pyomo
import importlib
import glob
import subprocess
from pyomo.common.timing import tic, toc
from smoek_models import pmedian1, pmedian2, pmedian3, pmedian4
from smoek.code.pyomo import generate as generate_pyomo
from smoek.code.coek import generate as generate_coek
from smoek import JsonDataPortal

codes = ['pyomo', 'coek1', 'coek2']
sizes = [1000, 3000]
#sizes = [100]
suffixes = ["lp", "nl"]
#tests = {"pmedian1": pmedian1, "pmedian2": pmedian2, 'pmedian3':pmedian3, 'pmedian4':pmedian4}
tests = {"pmedian1": pmedian1, 'pmedian3':pmedian3}
testdata = {'pmedian1':{}, 'pmedian3':dict(d="std::map<std::tuple<int,int>,double>")}
ntrials = 1


def collect_coek_models():
    if os.path.exists("models/smoek_generate.cpp"):
        os.remove("models/smoek_generate.cpp")
    os.chdir("models")
    testnames = [fname.split('.')[0] for fname in glob.glob("*.cpp")]
    os.chdir("..")

    with open("models/smoek_generate.cpp",'w') as OUTPUT:
        generate_fn = "\n".join(f'if (testname == "{name}") return generate_{name}(data);' for name in testnames)
        generate_decl = "\n".join(f'coek::CompactModel generate_{name}(const coek::DataPortal& data);' for name in testnames)

        testnames_set = f'std::set<std::string> testnames_set = {{ {",".join('"'+name+'"' for name in testnames)} }};'

        output = f"""
#include <set>
#include <string>
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

{testnames_set}

const std::set<std::string>& testnames() {{ return testnames_set; }}

{generate_decl}

coek::CompactModel generate(const std::string& testname, const coek::DataPortal& data)
{{
{generate_fn}

throw std::runtime_error("Unknown testname: " +testname);
}}
"""
        OUTPUT.write(output)


def run_pyomo(test, size, trial, suffix):
    print("-" * 70)
    tic(f"Test: {test} {size} {trial} {suffix}")

    data = JsonDataPortal()
    toc(f"Create JSON data portal")

    smoek_model = tests[test](size, data=data)
    toc("Smoek model generated")

    generate_pyomo(model=smoek_model, outfile=f"models/pyomo_{test}_{size}.py")
    toc(f"Pyomo model written: models/pyomo_{test}_{size}.py")

    if 'models' in sys.modules:
        del sys.modules['models']
    if f'models.pyomo_{test}_{size}' in sys.modules:
        del sys.modules[f'models.pyomo_{test}_{size}']
    module = importlib.import_module(f"models.pyomo_{test}_{size}")
    generate = getattr(module, f"generate_{test}")
    toc(f"Imported models/pyomo_{test}_{size}")

    if len(testdata[test]) > 0:
        jsonfile = f"data/{test}_{size}.json"
        data.load(jsonfile)
        toc(f"Loaded JSON data: {jsonfile}")

    pyomo_model = generate(data)
    toc("Pyomo model generated")
    
    fname = f"{suffix}files/code_pyomo_{test}_{size}_{trial}.{suffix}"
    pyomo_model.write(fname)
    toc(f"Writing file {fname}")

def run_coek1(test, size, trial, suffix):
    print("-" * 70)
    tic(f"Test: {test} {size} {trial} {suffix}")

    jsonfile = f"data/{test}_{size}.json" if len(testdata[test]) > 0 else ""
    data = JsonDataPortal(filename=jsonfile)
    toc(f"Create JSON data portal")

    smoek_model = tests[test](size, data=data)
    toc("Smoek model generated")

    generate_coek(model=smoek_model, model_name=f"{test}_{size}", outfile=f"models/{test}_{size}.cpp", data=testdata[test])
    toc(f"Coek model written: models/{test}_{size}.cpp")

    collect_coek_models()
    subprocess.run("make", cwd="build", shell=True, check=True)
    toc(f"Compiling runner")

    fname = f"{suffix}files/code_coek1_{test}_{size}_{trial}.{suffix}"
    subprocess.run(f"build/run {test}_{size} {size} {fname} 0 {jsonfile}", shell=True, check=True)
    toc(f"Writing file {fname}")

def run_coek2(test, size, trial):
    print("-" * 70)
    tic(f"Test: {test} {size} {trial} lp")

    jsonfile = f"data/{test}_{size}.json" if len(testdata[test]) > 0 else ""
    data = JsonDataPortal(filename=jsonfile)
    toc(f"Create JSON data portal")

    smoek_model = tests[test](size, data=data)
    toc("Smoek model generated")

    generate_coek(model=smoek_model, model_name=f"{test}_{size}", outfile=f"models/{test}_{size}.cpp", data=testdata[test])
    toc("Coek model written: models/{test}_{size}.cpp")

    collect_coek_models()
    subprocess.run("make", cwd="build", shell=True, check=True)
    toc(f"Compiling runner")

    fname = f"lpfiles/code_coek2_{test}_{size}_{trial}.lp"
    subprocess.run(f"build/run {test}_{size} {size} {fname} 1 {jsonfile}", shell=True, check=True)
    toc(f"Writing file {fname}")

def run(code, test, size, trial, suffix):
    if code == 'pyomo':
        run_pyomo(test, size, trial, suffix)
    elif code == 'coek1':
        run_coek1(test, size, trial, suffix)
    elif code == 'coek2':
        if (suffix == 'lp'):
            run_coek2(test, size, trial)
        else:
            print("-" * 70)
            print(f"WARNING: cannot run coek2 test using {suffix} suffix.")

code = 'coek1'
if len(sys.argv) == 2:
    code = sys.argv[1]

if False:
    run(code, 'pmedian1', 1000, 0, 'lp')
else:
    for pymodel in codes:
        for test in tests:
            for size in sizes:
                for trial in range(ntrials):
                    for suffix in suffixes:
                        run(pymodel, test, size, trial, suffix)
