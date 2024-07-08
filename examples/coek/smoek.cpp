#include <coek/coek.hpp>

coek::Model generate_simple1(coek::DataPortal& data);
coek::Model generate_knapsack1(coek::DataPortal& data);
coek::Model generate_knapsack2(coek::DataPortal& data);
coek::Model generate_knapsack3(coek::DataPortal& data);


int main(int argc, char** argv)
{
    if (argc == 1) {
        std::cout << "smoek <test-name> [<json-data-filename>]" << std::endl;
        return 0;
    }

    std::string testname;
    coek::DataPortal data;
    if (argc >= 2)
        testname = argv[1];   // filename
    if (argc >= 3) {
        data.load(argv[2]);
        }

    coek::Model model;
    if (testname == "simple1")
        model = generate_simple1(data);
    else if (testname == "knapsack1")
        model = generate_knapsack1(data);
    else if (testname == "knapsack2")
        model = generate_knapsack2(data);
    else if (testname == "knapsack3")
        model = generate_knapsack3(data);

    model.print_equations();
    model.write(testname+".lp");

    return 0;
}

