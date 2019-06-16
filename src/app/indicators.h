#ifndef INDICATORS_H_
#define INDICATORS_H_

#include <vector>
#include <string>

#include "parser.h"
#include "data.h"


typedef unsigned int u_int;


struct counter {
  std::vector<float> vec = std::vector<float>(VEC_LENGTH);
  std::vector<float> weights = std::vector<float>(VEC_LENGTH);

  void setWeights(u_int idx, u_int length, float* w) {
    for (u_int i = 0; i < length; i++)
      weights[idx + i] = w[i];
  }
};


class Indicator {
  public:
    virtual void increment(u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) = 0;
};


class Indicators {
  public:
    static void evaluate (u_int position,
                          std::vector<token>& sentence,
                          counter& cnt);
};

#endif
