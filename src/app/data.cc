#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <unordered_map>

#include "data.h"


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
  dataEntry de;
  bool quote = false;
  int start = -1;
  std::vector<std::string> split;

  for (u_int i = 0; i < line.length(); i++) {
    if (start == -1 && line[i] == quotechar) {
      quote = true;
    } else {
      quote = false;
    }

    if (start != -1 && line[i] == quotechar && line[i+1] != quotechar)
      quote = false;

    if (start == -1)
      start = i;

    if (!quote && line[i] == delimeter) {
      split.push_back(line.substr(start, i - start));
      start = -1;
    }
  }

  de.wa_word = unquote(split[0], quotechar);
  for (u_int i = 0; i < split.size(); i++)
    std::cout << i << ": " << split[i] << std::endl;
  int count = std::stoi(split[1]);
  std::vector<variation> vars(count);

  for (int i = 0; i < count; i++) {
    std::cout << "TODO: load vector" << std::endl;

  }

  return de;
}


void Data::loadData(char delimeter, char quotechar) {
  std::ifstream file(csvFileName);
  std::string line = "";
  // while (getline(file, line))
  //   numLines++;

  std::unordered_map<std::string, std::vector<variation>> dataMap;

  std::string wa_word;
  while (getline(file, line)) {
    dataEntry de = processLine(line, delimeter, quotechar);
    dataMap[de.wa_word] = de.vars;
  }
}
