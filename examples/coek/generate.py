import os
import smoek as smk
import smoek.core.tests.models as models
from smoek.code.coek import generate

if not os.path.exists("models"):
    os.mkdir("models")

testnames = ["small1", "small2", "small3", "small4", "small5", "small6",
                "testing1", "testing2", "testing4", "testing5", "testing6", "testing7",
                "simple1", "hs060",
                "knapsack1", "knapsack2", "knapsack3", "knapsack4",
                "pmedian1", "pmedian1_simple", "pmedian2"
]

namemap = {
    "pmedian1_simple": "pmedian1"
}

options = {
    "knapsack3": dict(data={"N":"int"}),
    "knapsack4": dict(data={"value":"std::map<int,double>", "weight":"std::map<int,double>", "capacity":"double", "ITEMS":"std::set<int>"}),
    "pmedian1_simple": dict(loops="simple")
}

for name in testnames:
    print(f"GENERATING models/{name}.cpp")
    testname = namemap.get(name,name)
    model = getattr(models, testname)()
    other_options = options.get(name,{}) 
    generate(model=model, outfile=f"models/{name}.cpp", model_name=name, **other_options)

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

