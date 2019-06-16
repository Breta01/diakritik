#ifndef HASHMAP_H_
#define HASHMAP_H_

#include <functional>
#include <string>
#include <vector>


// Prvočíslo o 30% větší než velikost slovníku (=1189376)
const int TABLE_SIZE = 1550027;

const int VEC_LENGTH = 70;
struct variant {
  std::string word;
  std::string tag;
  float vec[VEC_LENGTH];
};


typedef std::vector<variant> v_vec;
typedef unsigned long u_long;


class HashMap {
  /* Hash tabulka pomocí 3 vektorů
     TODO: Efektivně uložit a načíst vektory, aby se nemusela tabulka
           vytvářet při spuštění programu.
  */
  std::hash<std::string> hash;
  std::vector<std::string> keys = std::vector<std::string>(TABLE_SIZE);
  std::vector<v_vec> vals = std::vector<v_vec>(TABLE_SIZE);
  std::vector<bool> used = std::vector<bool>(TABLE_SIZE, false);

  public:
    v_vec* insert(std::string key);
    v_vec* get(std::string& key);
};

#endif
