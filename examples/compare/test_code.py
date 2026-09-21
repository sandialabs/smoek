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

codes = ["pyomo", "coek1", "coek2"]
sizes = [1000, 3000]
# sizes = [100]
suffixes = ["lp", "nl"]
# tests = {"pmedian1": pmedian1, "pmedian2": pmedian2, 'pmedian3':pmedian3, 'pmedian4':pmedian4}
tests = {"pmedian1": pmedian1, "pmedian3": pmedian3}
testdata = {"pmedian1": {}, "pmedian3": dict(d="std::map<std::tuple<int,int>,double>")}
ntrials = 1

if len(sys.argv) > 1:
    codes = [sys.argv[1]]
for code in codes:
    for test in tests:
        for size in sizes:
            for trial in range(ntrials):
                for suffix in suffixes:
                    res = subprocess.run(
                        f"time python run_code.py {code} {test} {size} {trial} {suffix}",
                        shell=True,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                    )
                    print(res.stdout.decode())
