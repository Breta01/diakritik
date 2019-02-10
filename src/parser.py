import os
import argparse

from alphabet import remove_accents


parser = argparse.ArgumentParser(
    description="Parse words and create files for application.")
parser.add_argument(
    '--path',
    default='../data/syn2015',
    help="Path to extracted Syn2015 file.")


class Word:
    def __init__(self, fields):
        self.word = fields[0]
        self.base = fields[1]
        self.tag = fields[2]

        # self.wa_word = remove_accents(self.word)

    def __str__(self):
        return ' '.join([self.word, self.tag])

    def __repr__(self):
        return self.word + ' - ' + self.tag[0]


class Dictionary:
    def __init__(self):
        self.dictionary = {}

    def add_word(self, wa_word, word):
        if wa_word in self.dictionary:
            if str(word) in self.dictionary[wa_word]:
                self.dictionary[wa_word][str(word)] += 1
            else:
                self.dictionary[wa_word][str(word)] = 1
        else:
            self.dictionary[wa_word] = {str(word): 1}

    def size(self):
        return len(self.dictionary)


def process_sentence(sentence, dictionary):
    print(sentence)
    for word in sentence:
        if word.tag[0] != 'Z':
            if word.word.isalpha():
                try:
                    dictionary.add_word(remove_accents(word.word), word)
                except:
                    pass
            #         print(word)
            # else:
            #         print(word)


def words_extract(path):
    dictionary = Dictionary()
    with open(path) as f:
        sentence = []
        for i, line in enumerate(f):
            if line[:2] == '<s':
                # print(i, "- start sentence")
                sentence = []

            if line.strip() == '</s>':
                process_sentence(sentence, dictionary)

            if line[0] != '<':
                fields = line.split('\t')
                sentence.append(Word(fields))

    print("END")
    print(dictionary.size())


if __name__ == "__main__":
    args = parser.parse_args()
    words_extract(args.path)
