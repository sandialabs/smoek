import sys
import os
import pyomo
import subprocess
from pyomo.common.timing import tic, toc
from smoek_models import pmedian1, pmedian2, pmedian3, pmedian4
from smoek.pymodel.pyomo import generate as generate_pyomo
from smoek.pymodel.poek import generate as generate_poek
from smoek import JsonDataPortal

sizes = [1000, 3000]
# sizes = [100]
suffixes = ["lp", "nl"]
exp = ["pyomo", "poek1", "poek2"]
# tests = {"pmedian1": pmedian1, "pmedian2": pmedian2, 'pmedian3':pmedian3, 'pmedian4':pmedian4}
tests = {"pmedian1": pmedian1, "pmedian3": pmedian3}
ntrials = 1

if len(sys.argv) > 1:
    exp = [sys.argv[1]]
for pymodel in exp:
    for test in tests:
        for size in sizes:
            for trial in range(ntrials):
                for suffix in suffixes:
                    res = subprocess.run(
                        f"time python run_pymodel.py {pymodel} {test} {size} {trial} {suffix}",
                        shell=True,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                    )
                    print(res.stdout.decode())
