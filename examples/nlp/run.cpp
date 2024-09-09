#include <cstddef>
#include <cassert>
#include <filesystem>
#include <set>
//#include <coek/coek.hpp>
#include <coek/util/DataPortal.hpp>
#include "IpStdCInterfaceTypes.h"
#include "loadlib.h"

//
// Logic to load ipopt
//

extern "C" {

static libHandle_t ipopt_handle = NULL;
static CreateIpoptProblem_func_t CreateIpoptProblem_func_ptr = 0;
static FreeIpoptProblem_func_t FreeIpoptProblem_func_ptr = 0;
static AddIpoptStrOption_func_t AddIpoptStrOption_func_ptr = 0;
static AddIpoptNumOption_func_t AddIpoptNumOption_func_ptr = 0;
static AddIpoptIntOption_func_t AddIpoptIntOption_func_ptr = 0;
/* OpenIpoptOutputFile_func_t OpenIpoptOutputFile_func_ptr=0; */
/* SetIpoptProblemScaling_func_t SetIpoptProblemScaling_func_ptr=0; */
static SetIntermediateCallback_func_t SetIntermediateCallback_func_ptr = 0;
static IpoptSolve_func_t IpoptSolve_func_ptr = 0;
}

int load_ipopt_library(const char* libname, std::string& error_message)
{
    char buf[1024];
    ipopt_handle = loadlib(libname, buf, 1024);
    if (ipopt_handle == NULL) {
        error_message = buf;
        return 1;
    }

    CreateIpoptProblem_func_ptr
        = (CreateIpoptProblem_func_t)getsym(ipopt_handle, "CreateIpoptProblem", buf, 256);
    FreeIpoptProblem_func_ptr
        = (FreeIpoptProblem_func_t)getsym(ipopt_handle, "FreeIpoptProblem", buf, 256);
    AddIpoptStrOption_func_ptr
        = (AddIpoptStrOption_func_t)getsym(ipopt_handle, "AddIpoptStrOption", buf, 256);
    AddIpoptNumOption_func_ptr
        = (AddIpoptNumOption_func_t)getsym(ipopt_handle, "AddIpoptNumOption", buf, 256);
    AddIpoptIntOption_func_ptr
        = (AddIpoptIntOption_func_t)getsym(ipopt_handle, "AddIpoptIntOption", buf, 256);
    // OpenIpoptOutputFile_func_ptr = (OpenIpoptOutputFile_func_t)getsym(ipopt_handle,
    // "OpenIpoptOutputFile", buf, 256); SetIpoptProblemScaling_func_ptr =
    // (SetIpoptProblemScaling_func_t)getsym(ipopt_handle, "SetIpoptProblemScaling", buf, 256);
    SetIntermediateCallback_func_ptr
        = (SetIntermediateCallback_func_t)getsym(ipopt_handle, "SetIntermediateCallback", buf, 256);
    IpoptSolve_func_ptr = (IpoptSolve_func_t)getsym(ipopt_handle, "IpoptSolve", buf, 256);

    return 0;
}

bool load_ipopt(std::string& error_message)
{
    std::string tmp;
#ifdef _MSC_VER
    int error_code = load_ipopt_library("libipopt-3.dll", tmp);
    if (error_code == 1) {
        error_message = "Failed to load libipopt-3.dll: " + tmp;
#else
    int error_code = load_ipopt_library("libipopt.so", tmp);
    if (error_code == 1) {
        error_message = "Failed to load libipopt.so: " + tmp;
#endif
        error_code = load_ipopt_library("libipopt.dylib", tmp);
    }
    if (error_code == 1) {
        error_message = error_message + "\nFailed to load libipopt.dylib: " + tmp;
    }
    return error_code == 0;
}

//
// Logic to run the selected solver
//

const std::set<std::string>& testnames();
IpoptProblem generate(const std::string& testname, const coek::DataPortal& data, CreateIpoptProblem_func_t func_ptr, std::vector<Number>& last_x, std::vector<Number>& last_g);

Number* array_ptr(std::vector<Number>& v)
{
    if (v.size() == 0)
        return 0;
    return &(v[0]);
}

void run(const std::string& testname, const coek::DataPortal& data, bool quiet)
{
std::vector<Number> last_x;
std::vector<Number> last_g;

auto app = generate(testname, data, CreateIpoptProblem_func_ptr, last_x, last_g);

Number last_objval;
enum ApplicationReturnStatus status;
status = (*IpoptSolve_func_ptr)(app, array_ptr(last_x), array_ptr(last_g), &last_objval, 0, 0, 0, 0);

std::cout << std::endl << std::endl
                  << "*** The final value of the objective function is " << last_objval << '.'
                  << std::endl;
std::cout << "Status: " << status << std::endl;

(*FreeIpoptProblem_func_ptr)(app);
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
    std::string jsonfile = "data/" + testname + ".json";
    run(testname, jsonfile, quiet);
}

//
// Main
//

int main(int argc, char** argv)
{
    if (argc == 1) {
        std::cout << "run <test-name> [<json-data-filename>]" << std::endl;
        return 0;
    }

    std::string error_message;
    if (not load_ipopt(error_message)) {
        std::cerr << "ERROR LOADING IPOPT: " << error_message << std::endl;
        return 1;
        }

    if (argc >= 2) {
        std::string testname = argv[1];
        const auto& container = testnames();
        if (container.find(testname) == container.end())
            std::cout << "Unknown testname: " << testname << std::endl;

        if (argc == 3)
            run(testname, argv[2]);
        else
            run(testname, argv[1]);
        }

    return 0;
}

