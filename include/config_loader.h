#ifndef CONFIG_LOADER_H
#define CONFIG_LOADER_H

#include "options.h"
class ConfigLoader {
public:
  ConfigLoader(Options options, std::string package_name);
  std::string load_envvars(std::string const & key);
  void load_metadata();
};
#endif
