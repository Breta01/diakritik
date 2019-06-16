#include <functional>
#include <string>
#include <iostream>
#include <vector>

#include "hashmap.h"


v_vec* HashMap::insert(std::string key) {
  // Vrací pointer do pole dat, pro rychlejší zápis
  u_long loc = hash(key) % keys.size();

  while(used[loc])
    loc = (loc+1) % keys.size();

  used[loc] = true;
  keys[loc] = key;
  return &vals[loc];
}


v_vec* HashMap::get(std::string& key) {
  u_long loc = hash(key) % keys.size();

  while(true) {
    if (!used[loc])
      return nullptr;

    if (keys[loc]==key)
      return &vals[loc];

    loc = (loc+1) % keys.size();
  }
}
