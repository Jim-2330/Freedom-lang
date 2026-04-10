#include <iostream>

#include "freedon_core.hpp"

int main() {
    auto v = freedon::version();
    std::cout << "Freedon Lang C++ stub v"
              << v.major << "." << v.minor << "." << v.patch
              << " (prototype placeholder)" << std::endl;
    return 0;
}

