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
from abc import ABC, abstractmethod

class Indicator(ABC):
    """Base class for all indicators."""
    def __init__(self, name, size):
        self.name = name
        self.vec_size = size

    @abstractmethod
    def increment(self, sentence, position):
        pass

    @staticmethod
    def get_total(self, tokens):
        total = 0
        for key in tokens:
            total += tokens[key].counter.get(self.name)[0]
        return total

    @staticmethod
    def get_vec(self):
        """Provide initial vector for counting."""
        # +1 space for total counter
        return (self.vec_size + 1) * [0]

    @staticmethod
    def finalize(self, tokens):
        total = self.get_total(tokens)
        for key in tokens:
            tokens[key].counter.normalize(self.name, total)


class OccurenceInd(Indicator):
    def __init__(self, name="occurence"):
        super().__init__(name, 1)

    @staticmethod
    def increment(self, sentence, position, token):
        token.counter.increment(self.name, 1);


class UppercaseInd(Indicator):
    def __init__(self, name="uppercase"):
        supre().__init__(name, 2)

    @staticmethod
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
        super().__init__(name, 1)
        self.maper = {
            '.': 1,
            '!': 2,
            '?': 3
        }

    @staticmethod
    def increment(self, sentence, position, token):
        symbol = None
        for i in range(1, 3):
            if sentence[-i].word in self.maper:
                symbol = sentence[-i].word

        if symbol is None:
            print("No correct end symbol of sentence found.")

        if self.maper[symbol] is not None:
            token.counter.increment(self.name, self.maper[symbol]);


class SpeechInd(Indicator):
    def __init__(self, name="speech"):
        supre().__init__(name, 2)

    @staticmethod
    def increment(self, sentence, position, token):
        pass



indicators = {
    "occurence": OccurenceInd()
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
        self.counter[name] = [i / total for i in self.counter[name]]

