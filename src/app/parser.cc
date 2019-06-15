#include <iostream>
#include <string>
#include <vector>

#include "parser.h"
#include "data.h"

Parser::Parser(std::string dataFile) {
  data = new Data(dataFile);
}

void Parser::processText(std::string& text) {
  std::cout << "Processing text:" << std::endl;
  text = text + " - EDITED";
  std::cout << text << std::endl;
}


