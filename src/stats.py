import csv
import math
import numpy as np
import os
import pickle

from alphabet import remove_accents
from indicators import indicators, IndicatorCounter, SpeechInd
from parser import Token

# TODO:
#     - Odstranit malo casta slova
#     - masking vectors by indicators
#     - close distance -> choose by frequency
#     - Rovnou tagovat podle nejpravdepodobnejsi
#     - Mřit jen nerozhodná slova


class DicEntry:
    def __init__(self, tag, vector):
        self.tag = tag
        self.vector = vector


def load_dic(path):
    vec_size = 0
    for key in indicators:
        vec_size += indicators[key].vec_size
    print('Vector legnth:', vec_size)

    dictionary = {}
    with open(path, 'r') as f:
        reader = csv.reader(
                f, delimiter=' ', quotechar='', quoting=csv.QUOTE_NONE)

        for line in reader:
            dictionary[line[0]] = {}

            if int(line[1]) == 1:
                dictionary[line[0]][line[2]] = DicEntry(line[3], None)
            else:
                for i in range(int(line[1])):
                    idx =  2 + i * (vec_size + 2)
                    tag = line[idx+1]
                    vector = [float(line[idx + 2 + v]) for v in range(vec_size)]
                    dictionary[line[0]][line[idx]] = DicEntry(tag, vector)

    return dictionary


dictionary = load_dic(
    os.path.join(os.path.dirname(__file__), 'obj/dictionary.dic'))

print('Number of dic entries words:', len(dictionary))
keys = list(dictionary.keys())
arr = np.array([len(dictionary[k]) for k in keys])
idx = np.argmax(arr)
print('Word with the most variations:')
print(dictionary[keys[idx]])

print('Number of words with x variations:')
for i in range(1, 11):
    print(str(i) + ':', sum(1 if len(dictionary[k]) == i else 0
                            for k in dictionary.keys()))

print('Number of mistakes - variations with low accuracy')
print('Četnost varianty: 1 %')
for i in range(2, 10):
    count = 0
    for k in dictionary.keys():
        if len(dictionary[k]) == i:
            for v in dictionary[k].values():
                if v.vector[1] < 0.01 and v.vector[0] < 5:
                    count += 1
                    break
    print(i, count)


print('Četnost varianty: 0.5 %')
for i in range(2, 10):
    count = 0
    for k in dictionary.keys():
        if len(dictionary[k]) == i:
            for v in dictionary[k].values():
                if v.vector[1] < 0.005 and v.vector[0] < 5:
                    count += 1
                    break
    print(i, count)


## FULL DATA EVALUAtion ##
def distance(v1, v2, mask):
    # dist = 0
    # for i in range(len(v1)):
    #     dist += mask[i] * ((v1[i] - v2[i]) ** 2)
    # return dist ** (1/2)

    minimum = min([abs(v1[i] - v2[i]) if mask[i] == 1 else 100
                   for i in range(1, len(v1))])
    return minimum + abs(v1[0] - v2[0])

    # return (1 - v1[0])


class Counter():
    def __init__(self):
        self.counter = IndicatorCounter()

    def update(self, sentence, position):
        for ind in indicators:
            indicators[ind].increment(sentence, position, self)

    def get_vector(self):
        return self.counter.get_vector()

class Word:
    def __init__(self, word):
        self.word = word.lower()
        self.org_word = word


def get_variation(sentence, word, position):
    counter = Counter()
    counter.update(sentence, position)
    vector = counter.get_vector()

    # mask = [0] + [1] * (len(vector) - 1)
    mask = [1] * (len(vector))
    if position == 0 or (position == 1 and sentence[0].tag[0] == 'Z'):
        mask[2] = 0

    res = []
    for key, item in dictionary[word.word].items():
        if res == [] or res[0] > distance(item.vector, vector, mask):
            res = [distance(item.vector, vector, mask), key]
    return res[1]


def simple_eval(sentence):
    new_sentence = []
    for position, word in enumerate(sentence):
        if word is None or word.word not in dictionary:
            new_sentence.append(word.word)
            continue

        if len(dictionary[word.word]) == 1:
            new_sentence.append(list(dictionary[word.word].keys())[0])
        else:
            variation = get_variation(sentence, word, position)

            new_word = ''.join(a.upper() if b.isupper() else a
                               for a, b in zip(variation, word.org_word))
            new_sentence.append(new_word)
    return new_sentence


def evaluate(path, sentence_evaluator):
    """Evalueate sentence_evaluator on SYN2015 corpus."""
    total = 0
    correct = 0

    with open(path, 'r') as f:
        num_lines = 140668456
        sentence = []
        position = 0
        speech = False

        for i, line in enumerate(f):
            if line.strip() == '</s>':
                test_sentence = []
                for w in sentence:
                    try:
                        w.word = remove_accents(w)
                        test_sentence.append(w)
                        # test_sentence.append(Word(remove_accents(w)))
                    except:
                        test_sentence.append(w)

                # Measuring
                result = sentence_evaluator(test_sentence)
                correct += sum([1 if (a == b.org_word) else 0
                                for a, b in zip(result, sentence)])
                total += len(sentence)

                sentence = []
                position = 0

            if line[0] != '<':
                fields = line.split('\t')
                # Revrite tag
                # fields[2] = dictionary[fields[0].lower]
                new_token = Token(fields, position, speech)
                sentence.append(new_token)
                if SpeechInd.is_speech(new_token.word):
                    speech = not speech
                position += 1

            if i % 100000 == 0:
                print('Acc %.5f: %r / %r' %
                      (correct / max(total, 1), i, num_lines), end='\r')

    print()
    print('Correct / Total: %r / %r' % (correct, max(total, 1)))
    print('Accuracy:', correct / total * 100)


if __name__ == '__main__':
    data_path = os.path.join(os.path.dirname(__file__), '../data/syn2015')
    evaluate(data_path, simple_eval)

