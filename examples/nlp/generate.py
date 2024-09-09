import os
import smoek as smk
import smoek.core.tests.models as models
from smoek.code.nlp import generate

if not os.path.exists("models"):
    os.mkdir("models")

testnames = ["small1", "small2", "small3", "small4", "small5", "small6",
                "testing1", "testing2", "testing4", "testing5", "testing6", "testing7",
                "simple1", "hs060",
#                "knapsack1", "knapsack2", "knapsack3", "knapsack4"
]

data = {
    "knapsack3": {"N":"int"},
    "knapsack4": {"value":"std::map<int,double>", "weight":"std::map<int,double>", "capacity":"double", "ITEMS":"std::set<int>"},
}

for name in testnames:
    print(f"GENERATING models/{name}.cpp")
    model = getattr(models, name)()
    data_option = data.get(name,{}) 
    generate(model=model, outfile=f"models/{name}.cpp", data=data_option)

with open("models/smoek_generate.cpp",'w') as OUTPUT:
    generate_fn = "\n".join(f'if (testname == "{name}") return generate_{name}(data, func_ptr, last_x, last_g);' for name in testnames)
    generate_decl = "\n".join(f'IpoptProblem generate_{name}(const coek::DataPortal& data, CreateIpoptProblem_func_t func_ptr, std::vector<Number>& last_x, std::vector<Number>& last_g);' for name in testnames)

    testnames_set = f'std::set<std::string> testnames_set = {{ {",".join('"'+name+'"' for name in testnames)} }};'

    output = f"""
#include <set>
#include <vector>
#include <string>
#include <coek/util/DataPortal.hpp>
#include "IpStdCInterfaceTypes.h"

{testnames_set}

const std::set<std::string>& testnames() {{ return testnames_set; }}

{generate_decl}

IpoptProblem generate(const std::string& testname, const coek::DataPortal& data, CreateIpoptProblem_func_t func_ptr, std::vector<Number>& last_x, std::vector<Number>& last_g)
{{
{generate_fn}

throw std::runtime_error("Unknown testname: " +testname);
}}
"""

    OUTPUT.write(output)

