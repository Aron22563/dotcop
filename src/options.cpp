#include "../include/options.h"
#include <string>
Options::Options(){
  this->help=0; 
  this->status=0; 
  this->list=0; 
  this->install = ""; 
  this->remove = ""; 
}
std::string Options::toString() {
    std::string res = "";
    res += std::string("Help: ") + (help ? "true" : "false") + std::string("\n");
    res += std::string("Status: ") + (status ? "true" : "false") + std::string("\n");
    res += std::string("List: ") + (list ? "true" : "false") + std::string("\n");
    res += std::string("Install: ") + install + "\n";
    res += std::string("Remove: ") + remove + "\n";
    return res;
}
