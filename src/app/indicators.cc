#include <iostream>
#include <vector>
#include <string>

#include "parser.h"
#include "indicators.h"
#include "data.h"

/* Template
class OccurenceInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 1;
      float weights[length] = {2};

      cnt.vec[idx] = 1;

      cnt.setWeights(idx, length, weights);

      return length;
    }
};
*/
class OccurenceInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 1;
      float weights[length] = {2};

      cnt.vec[idx] = 1;
      cnt.setWeights(idx, length, weights);
      return length;
    }
};


class UppercaseInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 2;
      float weights[length] = {5, 5};

      cnt.vec[idx + (sentence[idx].upper) ? 1 : 0] = 1;

      u_int i = 0;
      while (i < sentence.size() && sentence[i].tag[0] == 'Z')
        i++;

      if (pos > 0 and pos >= i)
        cnt.setWeights(idx, length, weights);
      return length;
    }
};


void Indicators::evaluate(u_int position,
                          std::vector<token>& sentence,
                          counter& cnt){
  u_int idx = 0;
  idx += OccurenceInd::increment(idx, position, sentence, cnt);
  idx += UppercaseInd::increment(idx, position, sentence, cnt);
}
