#ifndef DATA_H_
#define DATA_H_


const int VEC_LENGTH = 70;

struct variant {
  std::string word;
  std::string tag;
  float vec[VEC_LENGTH];
};


class Data {
  std::string csvFileName;
  std::unordered_map<std::string, std::vector<variant>> dataMap;

  struct dataEntry {
    std::string wa_word;
    std::vector<variant> vars;
  };

  public:
    Data(std::string csvFile) {
      csvFileName = csvFile;
      loadData();
    }

    std::vector<float> getWordVector(std::string word);
    std::string getWordTag(std::string word);

  private:
    void loadData(char delimeter=',', char quotechar='"');
    dataEntry processLine(std::string line,
                          char delimeter,
                          char quotechar);
    std::string unquote(std::string s, char quotechar='"');
};


#endif
