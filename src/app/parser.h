#ifndef PARSER_H_
#define PARSER_H_

#include <string>
#include "data.h"


class Parser {
  Data* data;

  struct token {
    std::string wa_word;
    std::string word;
    std::string tag;
  };

 public:
  Parser(std::string dataFile);
  void processText(std::string& text);

 private:
  void processLine(std::string& line);
  std::string getVariation(std::vector<token> line, int position);
};

#endif
