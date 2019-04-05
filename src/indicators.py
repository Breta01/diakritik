# (occurence, upper, lower, singular, plural, rod ...)

# def add_word(self, word):
#     # Occurence
#     self.vector[0] += 1
#     # Upper/Lower
#     if word.upper is not None:
#         self.vector[1 if word.upper else 2] += 1
#     # Singular/Plural
#     if word.singular is not None:
#         self.vector[3 if word.singular else 4] += 1
#     # Rod
#     # if word.rod is not None:
#     #     self.vector[5 + word.rod]

# TODO:
#    - normalization for other indicators
#    - contorl speech in sentences

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
    def __init__(self, name="occurence"):
        super().__init__(name, 1, 'rel')

    def increment(self, sentence, position, token):
        token.counter.increment(self.name, 1)


class UppercaseInd(Indicator):
    def __init__(self, name="uppercase"):
        super().__init__(name, 2, 'single_rel')

    def increment(self, sentence, position, token):
        if (position > 1 or
            (position == 1 and sentence[0].tag[0] != 'Z')):
            is_upper = sentence[position].org_word[0].isupper()
        else:
            is_upper = None

        if is_upper is not None:
            if is_upper:
                token.counter.increment(self.name, 1)
            else:
                token.counter.increment(self.name, 2)


class SentenceTypeInd(Indicator):
    def __init__(self, name="sentence_type"):
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
    def __init__(self, name="speech"):
        super().__init__(name, 2, 'single_rel')

    @staticmethod
    def is_speech(word):
        # Add more characters to check
        chars = ['"']
        return word in chars

    def increment(self, sentence, position, token):
        idx = 2 if sentence[position].speech else 1
        token.counter.increment(self.name, idx)



indicators = {
    "occurence": OccurenceInd(),
    "uppercase": UppercaseInd(),
    "sentence_type": SentenceTypeInd(),
    "speech": SpeechInd()
}


class IndicatorCounter:
    def __init__(self):
        self.counter = {}
        for ind in indicators:
            self.counter[ind] = indicators[ind].get_vec()

    def get(self, name):
        return self.counter[name]

    def increment(self, name, idx):
        """Increment indicator and total counter."""
        self.counter[name][idx] += 1
        self.counter[name][0] += 1

    def normalize(self, name, total):
        # print(self.counter[name])
        if total == 0:
            self.counter[name] = [0 for i in self.counter[name]]
        else:
            self.counter[name] = [i / total for i in self.counter[name]]

