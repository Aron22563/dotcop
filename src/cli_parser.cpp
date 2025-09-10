#include "../include/cli_parser.h"
#include "../include/options.h"

#include <ctype.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

CLIParser::CLIParser(int argc, char *argv[]) {
  Options options;
  parse_arguments(options, argc, argv);
  std::cout << options.toString();
}

void CLIParser::parse_arguments(Options &options, int argc, char *argv[]) {
  int index;
  opterr = 0;
  int c;
  while ((c = getopt(argc, argv, "hsli:r:")) != -1)
    switch (c) {
    case 'h':
      options.help = true;
      break;
    case 's':
      options.status = true;
      break;
    case 'l':
      options.list = true;
      break;
    case 'i':
      options.install = std::string(optarg);
      break;
    case 'r':
      options.remove = std::string(optarg);
      break;
    case '?':
      if (optopt != 0)
        std::cerr << "Option: " << optopt << " requires an argument!"
                  << std::endl;
      else if (isprint(optopt))
        std::cerr << "Unknown option: " << optopt << std::endl;
      else
        throw std::invalid_argument("Value parsing failed, exiting.");
    default:
      abort();
    }
}
