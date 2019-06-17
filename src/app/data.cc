#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <unordered_map>

#include "data.h"
#include "hashmap.h"


// TODO: Po získání pointru do hash tabulky asynchroně zpracovávat zbytek řádky


std::vector<variant>* Data::getWord(std::string word) {
  return dataMap.get(word);
}


void Data::loadData(char delimeter, char quotechar) {
  /* Načtení data z CSV souboru */
  std::ifstream file(csvFileName);
  std::string line = "";

  while (getline(file, line)) {
    processLine(line, delimeter);
  }
}


// std::string Data::unquote(std::string& s, char quotechar) {
//   if (s[0] == quotechar)
//     s = s.substr(1, s.length() - 2);
//
//   for (u_int i = 0; i < s.length(); i++) {
//     if (s[i] == quotechar) {
//       s.erase(i);
//       i++;
//     }
//   }
//   return s;
// }


void Data::processLine(std::string& line,
                       char delimeter) {
  /* Načítání jednotlivých řádků z data filu */
  std::vector<variant>* entry;
  int count, vec_i, var_i = -1, idx = 0, start = 0;
  std::vector<std::string> split;

  // Pole CSV souboru:
  // slovo, počet variant, varianta, tag, vec, (varianta, tag, vec)...
  for (u_int i = 0; i <= line.length(); i++) {
    if (i == line.length() || line[i] == delimeter) {
      if (idx == 0) {
        entry = dataMap.insert(line.substr(start, i - start));
      } else if (idx == 1) {
        count = std::stoi(line.substr(start, i - start));
        entry->resize(count);
      } else if ((idx - 2) % (VEC_LENGTH + 2) == 0) {
        var_i++;
        vec_i = 0;
        entry->at(var_i).word.assign(line, start, i - start);
      } else if ((idx - 3) % (VEC_LENGTH + 2) == 0) {
        entry->at(var_i).tag.assign(line, start, i - start);
      } else {
        entry->at(var_i).vec[vec_i] = std::stof(line.substr(start, i - start));
        vec_i++;
      }

      start = i+1;
      idx++;
    }
  }
}
