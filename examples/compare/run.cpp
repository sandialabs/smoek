#include <cassert>
#include <filesystem>
#include <set>
#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>
#include <coek/util/tictoc.hpp>

const std::set<std::string>& testnames();
coek::CompactModel generate(const std::string& testname, const coek::DataPortal& data);

void run(const std::string& testname, size_t size, const std::string& output_filename, bool compact_writer, const std::string& jsonfile, bool quiet=true)
{
coek::tic("Coek runner: " + testname + " " + std::to_string(size) + " " + output_filename + " " + jsonfile + " " + std::to_string(compact_writer));

coek::DataPortal data;
if (std::filesystem::exists(jsonfile)) {
    data.load_from_file(jsonfile);
    coek::toc("Loaded JSON data: "+jsonfile);
    }

const auto& container = testnames();
assert(container.find(testname) != container.end());
auto compact_model = generate(testname, data);
coek::toc("Created compact model");

if (compact_writer) {
    compact_model.write(output_filename);
    coek::toc("Wrote using compact model");
    }
else {
    auto model = compact_model.expand();
    if (not quiet)
        model.print_equations();
    model.write(output_filename);
    coek::toc("Wrote using expanded model");
    }
}

int main(int argc, char** argv)
{
    if (argc < 5) {
        std::cout << "run <test-name> <size> <output-file> <compact-write> [<json-data-filename>]" << std::endl;
        return 0;
    }

    std::string testname = argv[1];
    size_t size = atoi(argv[2]);
    std::string output_filename = argv[3];
    bool compact_writer = atoi(argv[4]);
    std::string jsonfile = "data/" + testname + "_" + std::to_string(size) + ".json";
    if (argc == 6)
        std::string jsonfile = argv[5];

    run(testname, size, output_filename, compact_writer, jsonfile);

    return 0;
}

