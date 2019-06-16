#ifndef DATA_H_
#define DATA_H_

#include <string>
#include <unordered_map>
#include <vector>

#include "hashmap.h"


class Data {
  std::string csvFileName;
  HashMap dataMap;

  struct dataEntry {
    std::string wa_word;
    std::vector<variant> vars;
  };

  public:
    Data(std::string csvFile) {
      csvFileName = csvFile;
      loadData();
    }

    std::vector<variant>* getWord(std::string word);

  private:
    void loadData(char delimeter=' ', char quotechar='"');
    void processLine(std::string& line,
                     char delimeter);
    /* std::string unquote(std::string& s, char quotechar='"'); */
};


#endif
