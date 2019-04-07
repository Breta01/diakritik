import argparse
import csv
import os
import pickle

from alphabet import remove_accents
from indicators import indicators, SpeechInd, IndicatorCounter
# from indicators import Indicator

# TODO:
#     - odstranit vektroy u slov s jednou variantou
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
    default=os.path.join(os.path.dirname(__file__), '../data/syn2015'),
    help="Path to extracted Syn2015 file.")


class Token:
    def __init__(self, fields, position, speech=False):
        self.position = position
        self.fields = fields
        self.word = fields[0].lower()
        self.org_word = fields[0]
        # self.base = fields[1]
        self.tag = fields[2]
        self.speech = speech
        # self.singular = self.tag[3] == 'S' if self.tag[3] != '-' else None

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


# Entry token indicators vals - udrzuji jednotlive hodnoty
# Indicatory, staticke, ktere spocitaji stat na vete a incrementuji token
class EntryToken(Token):
    def __init__(self, token):
        super().__init__(token.fields, token.position)
        self.counter = IndicatorCounter()

    def update(self, sentence, position):
        for ind in indicators:
            # print("Updating:", ind)
            indicators[ind].increment(sentence, position, self)

    def vector(self):
        return self.counter.get_vector()


class Entry:
    def __init__(self, wa_word, token):
        self.wa_word = wa_word
        self.tokens = {token.get_word(): EntryToken(token)}

    def no_accents(self):
        return self.wa_word

    def add_token(self, token):
        if not token.get_word() in self.tokens.keys():
            self.tokens[token.get_word()] = EntryToken(token)

    def finalize(self):
        for ind in indicators:
            indicators[ind].finalize(self.tokens)


class Dictionary:
    def __init__(self):
        self.dictionary = {}

    def add_token(self, wa_word, token, sentence, update=True):
        if not wa_word in self.dictionary:
            self.dictionary[wa_word] = Entry(wa_word, token)
        else:
            self.dictionary[wa_word].add_token(token)

        if update:
            self.dictionary[wa_word].tokens[token.get_word()].update(
                sentence, token.position)

    def size(self):
        return len(self.dictionary)


def save_words(dictionary):
    """Saving dictionary as:
    noaccents word, variations count, (for each variation: word, tag, vector)"""
    dic = dictionary.dictionary
    dic_path = os.path.join(os.path.dirname(__file__), 'obj/dictionary.dic')
    with open(dic_path, 'w') as f:
        writer = csv.writer(
            f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for key in sorted(list(dic.keys())):
            dic[key].finalize()

            row = [key, str(len(dic[key].tokens))]
            for t_entry in dic[key].tokens.values():
                row.extend([
                    t_entry.get_word(), t_entry.get_tag(), *t_entry.vector()])
            writer.writerow(row)


def process_sentence(sentence, dictionary):
    for token in sentence:
        if token.tag[0] != 'Z':
            if token.get_word().isalpha():
                try:
                    wa_word = remove_accents(token.get_word())
                except:
                    continue
                dictionary.add_token(wa_word, token, sentence)
        else:
            dictionary.add_token(token.get_word(), token, sentence, False)


def words_extract(path):
    dictionary = Dictionary()

    with open(path) as f:
        # Precalculated number of lines just for indication
        num_lines = 140668456

        sentence = []
        position = 0
        speech = False

        for i, line in enumerate(f):
            if line.strip() == '</s>':
                process_sentence(sentence, dictionary)
                sentence = []
                position = 0

            if line[0] != '<':
                fields = line.split('\t')
                new_token = Token(fields, position, speech)
                sentence.append(new_token)
                if SpeechInd.is_speech(new_token.word):
                    speech = not speech
                position += 1

            if i % 100000 == 0:
                print('Size %r: %r / %r' %
                      (dictionary.size(), i, num_lines), end='\r')

            # if i == 10000:
            #     break

    print()
    print('Number of words:', dictionary.size())
    # with open('obj/dictionary.pkl', 'wb') as f:
        # pickle.dump(dictionary.dictionary, f, 0)
    save_words(dictionary)



if __name__ == "__main__":
    args = parser.parse_args()
    words_extract(args.path)
