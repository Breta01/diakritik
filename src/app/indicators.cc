#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>

#include "parser.h"
#include "indicators.h"
#include "data.h"
#include "tagmapper.h"


class OccurenceInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 1;
      float weights[length] = {10};

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
      const u_int length = 1;
      float weights[length] = {4};

      cnt.vec[idx] = (sentence[pos].upper) ? 1 : 0;

      u_int i = 0;
      while (i < sentence.size() && sentence[i].tag[0] == 'Z') i++;

      if (pos > 0 and pos >= i)
        cnt.setWeights(idx, length, weights);
      return length;
    }
};


class SentenceTypeInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      char symbols[] = {'.', '!', '?'};
      const u_int length = 3;
      float weights[length] = {1, 1, 1};

      u_int i = sentence.size() - 1;
      while (i > 0 && sentence[i].tag == "ZW") i--;

      for (u_int x = 0; x < 3; x++) {
        if (sentence[i].wa_word[0] == symbols[x]) {
          cnt.vec[idx + x] = 1;
          cnt.setWeights(idx, length, weights);
        }
      }
      return length;
    }
};


class SpeechInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 1;
      float weights[length] = {2};

      cnt.vec[idx] = (sentence[pos].speech) ? 1 : 0;
      cnt.setWeights(idx, length, weights);
      return length;
    }
};


class CommaInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 1;
      float weights[length] = {2};

      u_int i = pos;
      bool comma = false;
      for (u_int i = 0; i < 3; i++) {
        if (pos >= i + 1 && sentence[pos - (i + 1)].word == ",") {
          comma = true;
        }
      }
      while (i > 0 && sentence[i].tag == "ZW") i--;

      cnt.vec[idx] = (comma) ? 1 : 0;
      cnt.setWeights(idx, length, weights);
      return length;
    }
};


class PositionInd {
  public:
    static u_int increment(u_int idx,
                          u_int pos,
                          std::vector<token>& sentence,
                          counter& cnt) {
      const u_int length = 3;
      float weights[length] = {1, 1, 1};

      u_int end = sentence.size() - 1;
      while (end > 0 && sentence[end].tag[0] == 'Z') end--;

      u_int start = 0;
      while (start < end && sentence[start].tag[0] == 'Z') start++;

      u_int i = 1;
      if (start < end) {
        if (pos == start) i = 0;
        else if (pos == end) i = 2;
      }

      cnt.vec[idx + i] = 1;
      cnt.setWeights(idx, length, weights);
      return length;
    }
};


class VerbInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 7;
      float weights[length] = {1, 1, 1, 1, 1, 1, 1};

      // Nalezení nejbližšího slovesa, které není infinitiv
      int dist = -1;
      std::string tag;

      for (int i = 0; i < (int)sentence.size(); i++) {
        if (sentence[i].tag[0] == 'V' &&
            sentence[i].tag[3] != '-') {
          if (dist == -1 || std::abs(i - (int)pos) < dist) {
            dist = std::abs(i - (int)pos);
            tag = sentence[i].tag;
          }
        }
      }

      if (dist != -1) {
        cnt.vec[idx + TagMapper::verbCisloMap(tag[3])] = 1;
        cnt.vec[idx + TagMapper::verbOsobaMap(tag[7])] = 1;
        cnt.setWeights(idx, length, weights);
      }

      return length;
    }
};


class PrevWordInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 22;
      float weights[length] = {0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                               0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                               0.1, 0.1, 0.1, 0.1};

      int prev = pos - 1;
      while (prev >= 0 && sentence[prev].tag == "ZW") prev--;

      if (prev >= 0) {
        std::string tag = sentence[prev].tag;
        cnt.vec[idx + TagMapper::druhMap(tag[0])] = 1;
        cnt.vec[idx + TagMapper::rodMap(tag[2])] = 1;
        cnt.vec[idx + TagMapper::cisloMap(tag[3])] = 1;
        cnt.vec[idx + TagMapper::padMap(tag[4])] = 1;

        cnt.setWeights(idx, length, weights);
      }

      return length;
    }
};


class NextWordInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 22;
      float weights[length] = {0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                               0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                               0.1, 0.1, 0.1, 0.1};

      u_int next = pos + 1;
      while (next < sentence.size() && sentence[next].tag == "ZW") next++;


      if (next < sentence.size()) {
        std::string tag = sentence[next].tag;
        cnt.vec[idx + TagMapper::druhMap(tag[0])] = 1;
        cnt.vec[idx + TagMapper::rodMap(tag[2])] = 1;
        cnt.vec[idx + TagMapper::cisloMap(tag[3])] = 1;
        cnt.vec[idx + TagMapper::padMap(tag[4])] = 1;

        cnt.setWeights(idx, length, weights);
      }

      return length;
    }
};


class PrepositionInd {
  public:
    static u_int increment(u_int idx,
                           u_int pos,
                           std::vector<token>& sentence,
                           counter& cnt) {
      const u_int length = 8;
      float weights[length] = {1, 1, 1, 1, 1, 1, 1, 1};

      for (u_int i = 0; i < 3; i++) {
        if (pos >= i + 1 && sentence[pos - (i + 1)].tag[0] == 'R') {
          char pad = sentence[pos - (i + 1)].tag[4];
          cnt.vec[idx + TagMapper::padMap(pad) - 14] = 1;
          cnt.setWeights(idx, length, weights);
        }
      }

      return length;
    }
};


void Indicators::evaluate(u_int position,
                          std::vector<token>& sentence,
                          counter& cnt){
  u_int idx = 0;
  idx += OccurenceInd::increment(idx, position, sentence, cnt);
  idx += UppercaseInd::increment(idx, position, sentence, cnt);
  idx += SentenceTypeInd::increment(idx, position, sentence, cnt);
  idx += SpeechInd::increment(idx, position, sentence, cnt);
  idx += CommaInd::increment(idx, position, sentence, cnt);
  idx += PositionInd::increment(idx, position, sentence, cnt);
  idx += VerbInd::increment(idx, position, sentence, cnt);
  idx += PrevWordInd::increment(idx, position, sentence, cnt);
  idx += NextWordInd::increment(idx, position, sentence, cnt);
  idx += PrepositionInd::increment(idx, position, sentence, cnt);
}
