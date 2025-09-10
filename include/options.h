#ifndef OPTIONS_H
#define OPTIONS_H

#include <string>

class Options {
public:
  // Constructors
  Options();
  // Variables
  bool help;
  bool status;
  bool list;
  std::string install;
  std::string remove;

  // Methods
  std::string toString();
};
#endif
