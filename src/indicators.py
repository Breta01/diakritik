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


class Indicator:
    def __init__(self):
        pass

    def finalize(self):
        pass

    def vector(self):
        pass
