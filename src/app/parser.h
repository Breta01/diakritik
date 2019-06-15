#ifndef PARSER_H_
#define PARSER_H_

#include <string>
#include "data.h"


typedef std::string::size_type str_size;
typedef unsigned int u_int;


struct token {
  std::string::size_type position;
  std::string org_word;
  std::string wa_word;
  std::string word;
  std::string tag;
  bool speech;
  bool upper;
  std::vector<variant>* variants;
};


class Parser {
  Data* data;
  char splitChars [29] = {' ', '!', '"', '#', '$', '&', '\'', '(', ')', '*', '+',
                          ',', '-', '.', '/', ':', ';', '=', '>', '?', '@', '[',
                          '\\', ']', '^', '_', '`', '\n', '\t'};
  char endChars [4] = {'.', '!', '?', '\n'};

  public:
    Parser(std::string dataFile);
    void processText(std::string& text);

  private:
    void processSentence(str_size start,
                         str_size end,
                         std::string& text,
                         std::string& orgText);
    void addToken(std::string word,
                  std::string::size_type pos,
                  bool speech,
                  std::vector<token>& sentence);
    std::string matchCase(std::string word, std::string org_word);
    std::string getVariant(u_int position,
                           std::vector<token>& sentence);
    double vecDistance(std::vector<float> a,
                       std::vector<float> b,
                       std::vector<float> weights);
};
#endif
