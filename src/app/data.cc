#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <unordered_map>

#include "data.h"


std::vector<variant>* Data::getWord(std::string word) {
  auto element = dataMap.find(word);

  if (element == dataMap.end()) {
    return nullptr;
  } else {
    return &(element->second);
  }
}


void Data::loadData(char delimeter, char quotechar) {
  /* Načtení data z CSV souboru */
  std::ifstream file(csvFileName);
  std::string line = "";

  dataMap.clear();

  while (getline(file, line)) {
    dataEntry entry = processLine(line, delimeter, quotechar);
    dataMap[entry.wa_word] = entry.vars;
  }
}


std::string Data::unquote(std::string s, char quotechar) {
  if (s[0] == quotechar)
    s = s.substr(1, s.length() - 2);

  for (u_int i = 0; i < s.length(); i++) {
    if (s[i] == quotechar) {
      s.erase(i);
      i++;
    }
  }

  return s;
}


Data::dataEntry Data::processLine(std::string line,
                                  char delimeter,
                                  char quotechar) {
  /* Načítání jednotlivých řádků z data filu */
  dataEntry entry;
  bool quote = false;
  int start = -1;
  std::vector<std::string> split;

  for (u_int i = 0; i < line.length(); i++) {
    if (start == -1 && line[i] == quotechar) {
      quote = true;
    }

    if ((start != -1 && line[i] == quotechar)
        && (i+1 >= line.length() || line[i+1] != quotechar)) {
      quote = false;
    }

    if (start == -1) {
      start = i;
    }

    if (!quote && line[i] == delimeter) {
      split.push_back(line.substr(start, i - start));
      start = -1;
    }
  }
  split.push_back(line.substr(start, line.length() - 1 - start));


  entry.wa_word = unquote(split[0], quotechar);
  int count = std::stoi(split[1]);
  std::vector<variant> variants(count);

  for (int i = 0; i < count; i++) {
    variants[i].word = unquote(split[2 + i*(VEC_LENGTH + 2)]);
    variants[i].tag = unquote(split[2 + i*(VEC_LENGTH + 2) + 1]);

    if (count > 1) {
      for (int x = 0; x < VEC_LENGTH; x++) {
        variants[i].vec[x] = std::stof(split[4 + i*(VEC_LENGTH + 2) + x]);
      }
    }
  }

  entry.vars = variants;

  return entry;
}
