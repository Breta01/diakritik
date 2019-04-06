import csv
import math
import numpy as np
import os
import pickle

from alphabet import remove_accents
from indicators import indicators, IndicatorCounter
from parser import Token

# TODO:
#     - masking vectors by indicators
#     - close distance -> choose by frequency



class DicEntry:
    def __init__(self, tag, vector):
        self.tag = tag
        self.vector = vector


def load_dic(path):
    vec_size = 0
    for key in indicators:
        vec_size += indicators[key].vec_size
    print(vec_size)

    dictionary = {}
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            dictionary[line[0]] = {}

            for i in range(len(line)):
                print(i, line[i])

            for i in range(int(line[1])):
                idx =  2 + i * (vec_size + 2)
                tag = line[idx+1]
                vector = [float(line[idx + 2 + v]) for v in range(vec_size)]
                dictionary[line[0]][line[idx]] = DicEntry(tag, vector)

    return dictionary



dictionary = load_dic(os.path.join(os.path.dirname(__file__), 'obj/dictionary.dic'))

print('Number of without accents words:', len(dictionary))
keys = list(dictionary.keys())
arr = np.array([len(dictionary[k]) for k in keys])
idx = np.argmax(arr)
print(dictionary[keys[idx]])

print('Number of words with x variations:')
for i in range(1, 11):
    print(str(i) + ':', sum(1 if len(dictionary[k]) == i else 0
                            for k in dictionary.keys()))

print('Number of mistakes - variations with low accuracy')
for i in range(2, 10):
    count = 0
    for k in dictionary.keys():
        if len(dictionary[k]) == i:
            s = sum(map(lambda x: x.vector[0], dictionary[k].values()))
            for v in dictionary[k].values():
                if v.vector[0] / s < 0.01 and v.vector[0] < 5:
                    # print(dictionary[k])
                    count += 1
                    break
    print(i, count)



## FULL DATA EVALUAtion ##
def distance(v1, v2, mask):
    dist = 0
    for i in range(len(v1)):
        dist += mask[i] * ((v1[i] - v2[i]) ** 2)
    return math.sqrt(dist)


class Counter():
    def __init__(self):
        self.counter = IndicatorCounter()

    def update(self, sentence, position):
        for ind in indicators:
            indicators[ind].increment(sentence, position, self)

    def get_vector(self):
        return counter.get_vector()


def get_variation(sentence, word, position):
    counter = Counter()
    counter.update(sentence, position)
    vector = counter.get_vector()

    mask = [0] + [1] * (len(vector) - 1)
    if position == 0:
        mask[1:3] = [0, 0]

    res = []
    for key, vec in dictionary[word.lower()].items():
        if res == [] or res[0] < dist(vec, vector, mask):
            res = [dist(vec, vector, mask), key]
    return res[1]


def simple_eval(sentence):
    new_sentence = []
    for position, word in enumerate(sentence):
        if word is None or word not in dictionary:
            new_sentence.append(word)
            continue

        variation = get_variation(sentence, word, position)

        new_word = ''.join(a.upper() if b.isupper() else a
                           for a, b in zip(m[1], word))
        new_sentence.append(new_word)
    return new_sentence


def evaluate(path, sentence_evaluator):
    """Evalueate sentence_evaluator on SYN2015 corpus."""
    total = 0
    correct = 0

    with open(path, 'r') as f:
        num_lines = 140668456
        sentence = []

        for i, line in enumerate(f):
            if line.strip() == '</s>':
                test_sentence = []
                for w in sentence:
                    try:
                        test_sentence.append(remove_accents(w))
                    except:
                        test_sentence.append(None)

                # Measuring
                result = sentence_evaluator(test_sentence)
                correct += sum([1 if (a is None or a == b) else 0
                                for a, b in zip(result, sentence)])
                total += len(sentence)

                sentence = []

            if line[0] != '<':
                fields = line.split('\t')
                sentence.append(fields[0])

            if i % 100000 == 0:
                print('Acc %.5f: %r / %r' %
                      (correct / max(total, 1), i, num_lines), end='\r')

    print()
    print('Correct / Total: %r / %r' % (correct, max(total, 1)))
    print('Accuracy:', correct / total * 100)


if __name__ == '__main__':
    data_path = os.path.join(os.path.dirname(__file__), '../data/syn2015')
    evaluate(data_path, simple_eval)

