import os
import argparse
import pickle

from alphabet import remove_accents


parser = argparse.ArgumentParser(
    description="Parse words and create files for application.")
parser.add_argument(
    '--path',
    default='../data/syn2015',
    help="Path to extracted Syn2015 file.")


class Word:
    def __init__(self, fields):
        self.word = fields[0].lower()
        self.base = fields[1]
        self.tag = fields[2]
        # (relative occurence, ...)
        self.vector = [1, 0, 0]

        # self.wa_word = remove_accents(self.word)

    def finalize_vec(self, total):
        self.vector[0] /= total
        return str(self.vector)

    def increment(self):
        self.vector[0] += 1

    def __str__(self):
        return self.word
        # return ' '.join([self.word, self.tag])

    def __repr__(self):
        return self.word + ' - ' + self.tag[0]


class Dictionary:
    def __init__(self):
        self.dictionary = {}

    def add_word(self, wa_word, word):
        if wa_word in self.dictionary:
            if str(word) in self.dictionary[wa_word]:
                self.dictionary[wa_word][str(word)].increment()
            else:
                self.dictionary[wa_word][str(word)] = word
        else:
            self.dictionary[wa_word] = {str(word): word}

    def size(self):
        return len(self.dictionary)


def save_words(dictionary):
    dic = dictionary.dictionary
    with open('obj/dictionary.dic', 'w') as f:
        for k in sorted(list(dic.keys())):
            f.write(k)
            total = sum([w.vector[0] for w in dic[k].values()])
            for w in dic[k].values():
                f.write(';' + ';'.join([w.word, w.tag, w.finalize_vec(total)]))
            f.write('\n')


def process_sentence(sentence, dictionary):
    # print(sentence)
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
        num_lines = 140668456
        sentence = []

        for i, line in enumerate(f):
            if line.strip() == '</s>':
                process_sentence(sentence, dictionary)
                sentence = []

            if line[0] != '<':
                fields = line.split('\t')
                sentence.append(Word(fields))

            if i % 100000 == 0:
                print('Size %r: %r / %r' %
                      (dictionary.size(), i, num_lines), end='\r')

    print()
    print('Number of words:', dictionary.size())
    with open('obj/dictionary.pkl', 'wb') as f:
        pickle.dump(dictionary.dictionary, f, 0)
    save_words(dictionary)



if __name__ == "__main__":
    args = parser.parse_args()
    words_extract(args.path)
