import os
import pickle
import numpy as np
import ast

from alphabet import remove_accents
from parser import Word



def load_dic(path):
    dictionary = {}
    with open(path, 'r') as f:
        for line in f:
            fields = line.strip().split(';')
            dictionary[fields[0]] = {}

            for i in range(1, len(fields), 3):
                dictionary[fields[0]][fields[i]] = ast.literal_eval(fields[i+2])
    return dictionary


with open('obj/dictionary.pkl', 'rb') as f:
    dictionary = pickle.load(f)

print('Number of without accents words:', len(dictionary))

l = list(dictionary.keys())
arr = np.array([len(dictionary[k]) for k in l])
idx = np.argmax(arr)
print(dictionary[l[idx]])

print('Number of words with x variations:')
for i in range(1, 11):
    print(str(i) + ':', sum(1 if len(dictionary[k]) == i else 0
                            for k in dictionary.keys()))


print('Mistakes versions')
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






dictionary = load_dic('obj/dictionary.dic')


def simple_eval(sentence):
    new_sentence = []
    for word in sentence:
        if word is None or word not in dictionary:
            new_sentence.append(word)
            continue

        m = []
        # print(dictionary[word.lower()])
        for k, v in dictionary[word.lower()].items():
            if m == [] or m[0] < v[0]:
                m = [v[0], k]

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
    evaluate('../data/syn2015', simple_eval)

