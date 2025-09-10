#ifndef CLI_PARSER_H
#define CLI_PARSER_H

#include "options.h"
class CLIParser {
public:
  CLIParser(int argc, char *argv[]);
  void parse_arguments(Options &options, int argc, char *argv[]);
};
#endif
