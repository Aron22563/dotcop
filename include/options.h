#ifndef OPTIONS_H
#define OPTIONS_H

#include <string> 

struct Options {
    bool help = false; 
    bool status = false; 
    bool list = false; 
    std::string install = ""; 
    std::string remove = ""; 
};
#endif 
