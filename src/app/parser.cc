#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
#include <locale>
#include <codecvt>

#include "parser.h"
#include "data.h"
#include "indicators.h"


Parser::Parser(std::string dataFile) {
  data = new Data(dataFile);
}


void Parser::processText(std::string& text) {
  // Rozdělení poodel \n a ".!?" na věty
  std::cout << "Processing text:" << std::endl;
  std::cout << text << std::endl;
  std::string orgText;
  orgText.assign(text);
  text.clear();

  str_size start = 0;
  for (str_size i = 0; i < orgText.size(); i++) {
    for (char& c : endChars) {
      if ((i == orgText.size()-1 && start < orgText.size()) ||
          orgText[i] == c) {
        processSentence(start, i+1, text, orgText);
        start = i+1;
        break;
      }
    }
  }
}


void Parser::addToken(std::string word,
                      str_size pos,
                      bool speech,
                      std::vector<token>& sentence) {
  if (word.size() != 0) {
    token tk;
    tk.org_word = word;
    tk.position = pos;
    tk.speech = speech;
    tk.upper = std::isupper(word[0]);

    std::transform(word.begin(), word.end(), word.begin(), ::tolower);
    tk.variants = data->getWord(word);

    if (tk.variants != nullptr) {
      tk.wa_word = word;
      tk.word = tk.variants->at(0).word;
      tk.tag = tk.variants->at(0).tag;
    } else if (word == " " || word == "\n" || word == "\t") {
      tk.wa_word = tk.org_word;
      tk.word = tk.org_word;
      tk.tag = "ZW";
    } else {
      tk.wa_word = tk.org_word;
      tk.word = tk.org_word;
      tk.tag = "X---------------";
    }
    sentence.push_back(tk);
  }
}


void Parser::processSentence(str_size start,
                             str_size end,
                             std::string& text,
                             std::string& orgText) {
  /* Rozdělení stringu na vector tokenů */
  std::vector<token> sentence;
  str_size st = start;
  bool speech = false;

  for (str_size i = start; i <= end; i++) {
    for (char& c : splitChars) {
      if ((i == end && st < end) || orgText[i] == c) {
        std::string word = orgText.substr(st, i - st);
        addToken(word, st, speech, sentence);

        if (i != end) {
          word = orgText.substr(i, 1);
          addToken(word, i, speech, sentence);
          if (word == "\"") speech = !speech;
        }

        st = i+1;
        break;
      }
    }
  }

  for (u_int i = 0; i < sentence.size(); i++) {
    if (sentence[i].variants == nullptr) {
      text.append(sentence[i].org_word);
    } else {
      std::string final_word = getVariant(i, sentence);
      std::cout << sentence[i].wa_word << " > " << final_word << std::endl;
      text.append(matchCase(final_word, sentence[i].org_word));
    }
  }
}


std::string Parser::matchCase(std::string word, std::string org_word) {
  /* Změna velikosti písmen podle původního vstupu */
  std::wstring word32;
  std::wstring_convert<std::codecvt_utf8<wchar_t>> cvt;
  std::locale loc = std::locale("cs_CZ.utf8");
  std::string res_word;

  word32 = cvt.from_bytes(word);
  for (u_int i = 0; i < org_word.size(); i++) {
    if (std::isupper(org_word[i])) {
      res_word.append(cvt.to_bytes(std::toupper(word32[i], loc)));
    } else {
      res_word.append(cvt.to_bytes(word32[i]));
    }
  }

  return res_word;
}


double Parser::vecDistance(std::vector<float> a,
                           std::vector<float> b,
                           std::vector<float> mask) {
  double sum = 0;
  for (u_int i = 0; i < a.size(); i++) {
    sum += mask[i] * (1 - std::pow((double)(a[i] - b[i]), 2));
  }
  return std::sqrt(sum);
}


std::string Parser::getVariant(u_int position, std::vector<token>& sentence) {
  // Aplikace indikátorů, spočítání vzdáleností, vrácení nejbližší
  // Test vracení nejpravděpodobnějšího výstupu:
  counter cnt;
  return sentence[position].word;
}


