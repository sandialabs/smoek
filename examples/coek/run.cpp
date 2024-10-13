#include <cassert>
#include <filesystem>
#include <set>
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>

const std::set<std::string>& testnames();
coek::CompactModel generate(const std::string& testname, const coek::DataPortal& data);

void run(const std::string& testname, const coek::DataPortal& data, bool quiet=false)
{
const auto& container = testnames();
assert(container.find(testname) != container.end());
auto compact_model = generate(testname, data);
auto model = compact_model.expand();
if (not quiet)
    model.print_equations();
model.write("../models/"+testname+".nl");
}

void run(const std::string& testname, const std::string& jsonfile, bool quiet=false)
{
    coek::DataPortal data;
    if (std::filesystem::exists(jsonfile))
        data.load_from_file(jsonfile);
    run(testname, data, quiet);
}

void run(const std::string& testname, bool quiet=false)
{
    std::string jsonfile = "../data/" + testname + ".json";
    run(testname, jsonfile, quiet);
}

int main(int argc, char** argv)
{
    if (argc == 1) {
        std::cout << "smoek <test-name> [<json-data-filename>]" << std::endl;
        return 0;
    }

    if (argc == 2) {
        std::string testname = argv[1];
        const auto& container = testnames();
        if (container.find(testname) != container.end()) {
            run(testname);
        }
        else if (testname == "all") {
            for (auto& name: testnames()) {
                std::cout << "TEST " << name << std::endl;
                run(name, true);
            }
        }
        else
            std::cout << "Unknown testname: " << testname << std::endl;
        }

    else if (argc == 3) {
        std::string testname = argv[1];
        std::string jsonfile = argv[2];
        run(testname, jsonfile);
        }

    return 0;
}

