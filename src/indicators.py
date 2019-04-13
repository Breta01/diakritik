# TODO:
#    - Return mask z Indicatoru

from abc import ABC, abstractmethod

class Indicator(ABC):
    """Base class for all indicators."""
    def __init__(self, name, size, norm_type):
        """Inicialization of Indicator parent class
        Args:
            name - uniqe indentificator
            size - size of indicecs in vector
            norm_type - type of normalization ('rel' or 'single_rel')
        """
        self.name = name
        self.vec_size = size
        self.norm_type = norm_type

    @abstractmethod
    def increment(self, sentence, position, token):
        pass

    def get_total(self, tokens):
        total = 0
        for key in tokens:
            total += tokens[key].counter.get(self.name)[0]
        return total

    def get_vec(self):
        """Provide initial vector for counting."""
        # +1 space for total counter
        return (self.vec_size + 1) * [0]

    def finalize(self, tokens):
        if self.norm_type == 'rel':
            total = self.get_total(tokens)
            for key in tokens:
                tokens[key].counter.normalize(self.name, total)
        elif self.norm_type == 'single_rel':
            for key in tokens:
                total = tokens[key].counter.get(self.name)[0]
                tokens[key].counter.normalize(self.name, total)
        else:
            print("Unsupported normalization type.")


class OccurenceInd(Indicator):
    def __init__(self, name='occurence'):
        super().__init__(name, 1, 'rel')

    def increment(self, sentence, position, token):
        token.counter.increment(self.name, 1)


class UppercaseInd(Indicator):
    def __init__(self, name='uppercase'):
        super().__init__(name, 1, 'single_rel')

    def increment(self, sentence, position, token):
        idx = 0
        while sentence[idx].tag[0] == 'Z': idx += 1

        if (position > 0 and position >= idx):
            is_upper = sentence[position].org_word[0].isupper()
        else:
            is_upper = None

        if is_upper is not None:
            token.counter.increment(self.name, 1, 1 if is_upper else 0)


class SentenceTypeInd(Indicator):
    def __init__(self, name='sentence_type'):
        super().__init__(name, 3, 'single_rel')
        self.maper = {
            '.': 1,
            '!': 2,
            '?': 3
        }

    def increment(self, sentence, position, token):
        symbol = None
        for i in range(1, min(3, len(sentence)-1)):
            if sentence[-i].word in self.maper:
                symbol = sentence[-i].word

        if symbol is not None:
            token.counter.increment(self.name, self.maper[symbol])
        else:
            pass
            # print("No correct end symbol found.")


class SpeechInd(Indicator):
    def __init__(self, name='speech'):
        super().__init__(name, 1, 'single_rel')

    @staticmethod
    def is_speech(word):
        # Add more characters to check
        chars = ['"']
        return word in chars

    def increment(self, sentence, position, token):
        token.counter.increment(
            self.name, 1, 1 if sentence[position].speech else 0)


class CommaInd(Indicator):
    def __init__(self, name='comma'):
        super().__init__(name, 1, 'single_rel')

    def increment(self, sentence, position, token):
        comma = False
        if position != 0:
            for i in range(position-1, max(0, position-3), -1):
                if sentence[i].word == ',':
                    comma = True
                    break

        token.counter.increment(self.name, 1, 1 if comma else 0)


class PositionInd(Indicator):
    def __init__(self, name='position'):
        super().__init__(name, 3, 'single_rel')

    def increment(self, sentence, position, token):
        start = 0
        end = len(sentence) - 1
        while start < len(sentence) and sentence[start].tag[0] == 'Z':
            start += 1
        while end >= 0 and sentence[end].tag[0] == 'Z':
            end -= 1

        idx = 2
        if start < end:
            if position == start:
                idx = 0
            elif position == end:
                idx = 3

        token.counter.increment(self.name, idx)


class VerbInd(Indicator):
    def __init__(self, name='verb'):
        super().__init__(name, 7, 'single_rel')
        self.cislo_map = {'-': 1, 'S': 2, 'P': 3}
        self.osoba_map = {'-': 4, '1': 5, '2': 6, '3': 7}

    def find_verb(self, sentence, position):
        verbs = []
        for i, w in enumerate(sentence):
            if w.tag[0] == 'V':
                verbs.append((i, w))

        # Odstranění infinitivů
        if len(verbs) > 1:
            new_verbs = []
            for v in verbs:
                if v[1].tag[3] != '-' and v[1].tag[7] != '-':
                    new_verbs.append(v)
            verbs = new_verbs

        if len(verbs) == 0:
            return None
        if len(verbs) == 1:
            return verbs[0][1]

        return min(verbs, key=lambda x: abs(x[0] - position))[1]

    def increment(self, sentence, position, token):
        prob_verb = self.find_verb(sentence, position)
        if prob_verb is not None:
            token.counter.increment(
                self.name,
                [self.cislo_map.get(prob_verb.tag[3], 1),
                 self.osoba_map.get(prob_verb.tag[7], 1)])


class PrevWordInd(Indicator):
    def __init__(self, name='prev_word'):
        super().__init__(name, 22, 'single_rel')
        self.druh_map = {'-': 1, 'N': 2, 'A': 3, 'P': 4, 'C': 5}
        self.rod_map = {'-': 6, 'F': 7, 'I': 8, 'M': 9, 'N': 10}
        self.cislo_map = {'-': 11, 'D': 12, 'P': 13, 'S': 14}
        self.pad_map = lambda x: 15 + (int(x) if not x in ['-', 'X'] else 0)

    def increment(self, sentence, position, token):
        if position != 0:
            tag = sentence[position - 1].tag
            idx = [self.druh_map.get(tag[0], 1),
                   self.rod_map.get(tag[2], 6),
                   self.cislo_map.get(tag[3], 11),
                   self.pad_map(tag[4])]
            token.counter.increment(self.name, idx)


class NextWordInd(PrevWordInd):
    def __init__(self, name='next_word'):
        super().__init__(name)

    def increment(self, sentence, position, token):
        if position != len(sentence) - 1:
            tag = sentence[position + 1].tag
            idx = [self.druh_map.get(tag[0], 1),
                   self.rod_map.get(tag[2], 6),
                   self.cislo_map.get(tag[3], 11),
                   self.pad_map(tag[4])]
            token.counter.increment(self.name, idx)


class PrepositionInd(Indicator):
    def __init__(self, name='preposition'):
        super().__init__(name, 8, 'single_rel')
        self.pad_map = lambda x: 1 + (int(x) if not x in ['-', 'X'] else 0)

    def increment(self, sentence, position, token):
        if position != 0:
            for i in range(position-1, max(-1, position-3), -1):
                if sentence[i].tag[0] == 'R':
                    token.counter.increment(
                        self.name, self.pad_map(sentence[i].tag[4]), 1)
                    break


indicators = {
    "occurence": OccurenceInd(),
    "uppercase": UppercaseInd(),
    "sentence_type": SentenceTypeInd(),
    "speech": SpeechInd(),
    "comma": CommaInd(),
    "position": PositionInd(),
    "verb": VerbInd(),
    "prev_word": PrevWordInd(),
    "next_word": NextWordInd(),
    "preposition": PrepositionInd()
}


class IndicatorCounter:
    def __init__(self):
        self.counter = {}
        for ind in indicators:
            self.counter[ind] = indicators[ind].get_vec()

    def get(self, name):
        return self.counter[name]

    def increment(self, name, idx, val=1):
        """Increment indicator and total counter."""
        if type(idx) != list:
            idx = [idx]
        for i in idx:
            self.counter[name][i] += val
        self.counter[name][0] += 1

    def normalize(self, name, total):
        # print(self.counter[name])
        if total == 0:
            self.counter[name] = [0 for i in self.counter[name]]
        else:
            self.counter[name] = [i / total for i in self.counter[name]]

    def get_vector(self):
        vector = []
        for ind in indicators:
            vector.extend(self.counter[ind][1:])
        return vector

