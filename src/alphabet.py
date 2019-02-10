"""Helper functions for parsing of words."""

char_map = {'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e', 'í': 'i',
            'ň': 'n', 'ó': 'o', 'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u',
            'ů': 'u', 'ý': 'y', 'ž': 'z',
            'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E', 'Í': 'I',
            'Ň': 'N', 'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U',
            'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z'}


def _remove_char_accents(char):
    if (64 < ord(char) < 91 or
            96 < ord(char) < 123 or
            47 < ord(char) < 58):
        return char
    else:
        return char_map[char]


def remove_accents(word):
    return ''.join(_remove_char_accents(c) for c in word)
