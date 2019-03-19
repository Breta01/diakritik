import os
import argparse
import pickle

from alphabet import remove_accents

# TODO:
#     - udělat classy pro vlastnosti
#     - vlastnosti podle predchoziho slova
#     - prumerna vlastnost vety
#     - maskovani vlastnosti
#     - slovesa, detekce (vlastnosti, ztah ke slovum)
#     - nejblizsi podstatne jmeno
#     - Parser?


parser = argparse.ArgumentParser(
    description="Parse words and create files for application.")
parser.add_argument(
    '--path',
    default='../data/syn2015',
    help="Path to extracted Syn2015 file.")


class Token:
    def __init__(self, fields, position):
        self.positon = position
        self.word = fields[0].lower()
        self.base = fields[1]
        self.tag = fields[2]

        self.upper = fields[0].isupper() if position != 1 else None
        self.singular = self.tag[3] == 'S' if self.tag[3] != '-' else None

    def get_rod(self):
        return self.tag[2]

    def get_tag(self):
        return self.tag

    def get_word(self):
        return self.word

    def __str__(self):
        return self.word
        # return ' '.join([self.word, self.tag])

    def __repr__(self):
        return self.word + ' - ' + self.tag[0]


class Entry:
    def __init__(self, wa_word, token):
        self.wa_word = wa_word
        self.token = token
        self.indicators = {}

    def no_accents(self):
        return self.wa_word

    def word(self):
        return self.token.get_word()

    def tag(self):
        return self.token.get_tag()

    def add_indicators(self, indicators):
        for name, val in indicators:
            add_ind(name, val)

    def add_ind(self, name, value):
        if name in self.indicators:
            self.indicators[name].increment(value)

    def finalize_vec(self, total):
        # Poscitat procenta pres vsechny varianty slova
        # total[0] = sum([w.vector[0] for w in dic[k].values()])
        vector = []
        for name in self.indicators.keys():
            self.indicators[name].finalize()
            vector.append(self.indicators[name].vector())
        return str(vector)


class Dictionary:
    def __init__(self):
        self.dictionary = {}

    def add_entry(self, entry, indicators):
        word = entry.word()
        wa_word = entry.no_accents()
        if not wa_word in self.dictionary:
            self.dictionary[wa_word] = {word: entry}
        elif not word in self.dictionary[wa_word]:
            self.dictionary[wa_word][word] = entry

        self.dictionary[wa_word][word].add_indicators(indicators)

    def size(self):
        return len(self.dictionary)


def save_words(dictionary):
    dic = dictionary.dictionary
    with open('obj/dictionary.dic', 'w') as f:
        for key in sorted(list(dic.keys())):
            f.write(key)
            for entry in dic[key].values():
                f.write(';')
                f.write(';'.join([entry.get_word(),
                                  entry.tag(),
                                  entry.finalize_vec(total)]))
            f.write('\n')


def process_sentence(sentence, dictionary):
    for i, token in enumerate(sentence):
        if token.tag[0] != 'Z':
            if token.get_word().isalpha():
                try:
                    entry = Entry(remove_accents(token.get_word()), token)
                    dictionary.add_entry(entry)
                except:
                    pass
            #         print(word)
            # else:
            #         print(word)


def words_extract(path):
    dictionary = Dictionary()

    with open(path) as f:
        # Precalculated just for indication
        num_lines = 140668456

        sentence = []
        position = 0

        for i, line in enumerate(f):
            if line.strip() == '</s>':
                process_sentence(sentence, dictionary)
                sentence = []
                position = 0

            if line[0] != '<':
                fields = line.split('\t')
                position += 1
                sentence.append(Word(fields, position))

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
