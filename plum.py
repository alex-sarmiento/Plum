# Simple data structure that stores a dictionary and implements word searches.

import re


# Must not be lowercase letters or dot '.'.
_FIRST = "^"
_LAST = "$"


class WordsError(Exception):
    """
    Class for locally defined errors.
    """

    @classmethod
    def BadInputLetters(cls):
        return cls("input must only contain lowercase letters a-z")

    @classmethod
    def BadInputLettersAndDot(cls):
        return cls("input must only contain lowercase letters a-z and dots '.'")


class _Trie:

    def __init__(self, letter):
        """
        Initialize structure with one letter.
        """
        assert len(letter) == 1
        self._letter = letter
        self._entry = {}

    def add_word(self, word):
        """
        Adds a word into the data structure. Input has been sanitized.
        :type word: str
        :rtype: void
        """
        assert word[0] == self._letter
        if len(word) == 1:
            return

        left_letter = word[1]
        right_word = word[1:]
        if left_letter not in self._entry:
            self._entry[left_letter] = _Trie(left_letter)
        self._entry[left_letter].add_word(right_word)

    def contains(self, word):
        """
        Returns if the word is in the data structure. Input has been sanitized.
        :type word: str
        :rtype: bool
        """
        if len(word) == 1:
            return word[0] == self._letter

        left_letter = word[1]
        right_word = word[1:]
        if left_letter != ".":
            if left_letter not in self._entry:
                return False
            return self._entry[left_letter].contains(right_word)

        return any(self._entry[c].contains(right_word) for c in self._entry)

    def search(self, word, prefix):
        """
        Returns a list of words that have the exact word as a prefix.
        Input has been sanitized.
        :type word: str
        :type prefix: str
        :rtype: list
        """
        assert len(word) >= 1

        left_letter = word[1]
        right_word = word[1:]
        if left_letter != _LAST:
            if left_letter not in self._entry:
                return []
            return self._entry[left_letter].search(right_word, prefix)

        return ['%s%s' % (prefix, s) for s in self._get_all_suffixes()]

    def _get_all_suffixes(self):
        """
        Returns all suffixes from the current node.
        """
        all_suffixes = []
        for c in self._entry:
            if c == _LAST:
                all_suffixes.append("")
            else:
                all_suffixes.extend(
                    '%s%s' % (c, s) for s in self._entry[c]._get_all_suffixes())
        return all_suffixes


class Words:
    """
    Class that stores a dictionary and implements word searches.
    Internally, all patterns are bounded by special first and last characters.
    """

    _LETTERS_PATTERN = r"^[a-z]*$"
    _LETTERS_AND_DOT_PATTERN = r"^[a-z\.]*$"


    def __init__(self):
        """
        Initialize your data structure here.
        """
        self._trie = _Trie(_FIRST)

    def add_word(self, word):
        """
        Adds a word into the data structure.
        :type word: str
        :rtype: void
        """
        if not re.match(self._LETTERS_PATTERN, word):
            raise WordsError.BadInputLetters()
        self._trie.add_word(self._pad_word(word))

    def contains(self, word):
        """
        Returns if the word is in the data structure.
        A word could contain the dot character '.' to represent any one letter.
        :type word: str
        :rtype: bool
        """
        if not re.match(self._LETTERS_AND_DOT_PATTERN, word):
            raise WordsError.BadInputLettersAndDot()
        return self._trie.contains(self._pad_word(word))

    def search(self, word):
        """
        Returns a list of words that have the exact word as a prefix.
        If word contains a dot character '.' raise an Exception.
        :type word: str
        :rtype: list
        """
        if not re.match(self._LETTERS_PATTERN, word):
            raise WordsError.BadInputLetters()
        return self._trie.search(self._pad_word(word), word)

    def _pad_word(self, word):
        """
        Returns the input word with added markers at the beginning and end.
        :type word: str
        :rtype: str
        """
        return "%s%s%s" % (_FIRST, word, _LAST)


def DoExamples():
    words = Words()
    print(words.add_word("bad"))
    print(words.add_word("dad"))
    print(words.add_word("mad"))
    print(words.add_word("magic"))
    print(words.contains("pad"))
    print(words.contains("bad"))
    print(words.contains(".ad"))
    print(words.contains("b.."))
    print(words.search("ma"))
    print(words.search("mag"))
    print(words.search("g"))
    try:
        words.search(".ad")
    except WordsError as e:
        print('Exception: %s' % e)


def DoMoreExamples():
    words = Words()
    print(words.add_word("mad"))
    print(words.add_word("madmax"))
    print(words.search("mad"))
    print(words.contains(""))
    print(words.search(""))
    print(words.add_word(""))
    print(words.contains(""))
    print(words.search(""))
    try:
        words.contains("$")
    except WordsError as e:
        print('Exception: %s' % e)


def main():
    DoExamples()
    print("--------------------------------")
    DoMoreExamples()


if __name__ == "__main__":
    main()
