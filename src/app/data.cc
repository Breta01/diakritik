#include <iosream>
#include <string>
#include <fstream>
#include <vector>
#include <unordered_map>



int VEC_LENGTH = 70;

struct variation {
  std::string word;
  std::string tag;
  float vec[VEC_LENGTH];
}


class Data {
  std::string csvFileName;

  struct dataEntry {
    std::string wa_word;
    std::vector<variation> vars;
  }

  public:
    Data(std::string csvFile) {
      csvFileName = csvFile;
      loadData()
    };

    std::vector<float> getWordVector(std::string word);
    std::string getWordTag(str::string word);

  private:
    void loadData(std::string delimeter, std::string quotechar);
    dataEntry processLine(std::string line,
                          std::string delimeter,
                          std::string quotechar);
    std::string unquote(std::string s);
};


std::string unquote(std::string s, std::string quotechar="\"") {
  if (s[0] == quotechar)
    s = s.substr(1, s.length() - 2);

  for (int i = 0; i < s.length(); i++) {
    if (s[i] == quotechar) {
      str.erase(i);
      i++;
    }
  }

  return s;
}


dataEntry Data::processLine(std::string line,
                            std::string delimeter=",",
                            std::string quotechar="\"") {
  dataEntry de;
  bool quote = false;
  int start = -1, end;
  std::vector<std::string> split;

  for (int i = 0; i < line.length(); i++) {
    if (start == -1 && line[i] == quotechar) {
      quote = true;
    } else {
      quote = false;
    }

    if (start != -1 && line[i] == quotechar && line[i+1] != quotechar)
      quote = false

    if (start == -1)
      start = i;

    if (!quote && line[i] == delimeter) {
      split.push_back(line.substr(start, i - start));
    }
  }

  de.wa_word = unquote(split[0], quotechar);
  int count = std::stoi(split[1]);
  std::vector<variation> vars(count);

  for (int i = 0; i < count; i++) {




  }
}


void Data::loadData(std::string delimeter=",", std::string quotechar="\"") {
  std::ifstream file(csvFileName);
  std::string line = "";
  // while (getline(file, line))
  //   numLines++;

  std::unordered_map<std::string, vector<variation> dataMap;

  string wa_word;
  while (getline(file, line)) {
    dataEntry de = processLine(line, delimeter, quotechar);
    unordered_map[de.wa_word] = de.vars;
  }
}

