from __future__ import annotations
import string
from collections import Counter

class PositionalRequirements:
    def __init__(self) -> None:
        self.required = ''
        self.banned = []

    def __str__(self):
        return f"PositionalRequirements: required: {self.required}; banned: {self.banned}"


class Constraints:
    def __init__(self, length: int) -> None:
        self.letter_counts = {letter: [0, 5] for letter in string.ascii_uppercase}
        self.positional_requirements = [PositionalRequirements()] * length

    def __str__(self):
        return f"Constraints: {self.positional_requirements}; {self.letter_counts}"


class Word:
    def __init__(self, word: str) -> None:
        self.positional = word.split()
        self.letter_counts = {letter: count for letter, count in Counter(word).items()}
    def __str__(self):
        return "".join(self.positional)

    def is_valid(self, constraints: Constraints) -> bool:
        try:
            for i, position in enumerate(self.positional):
                if constraints.positional_requirements[i].required and constraints.positional_requirements[i].required != position:
                        return False
                else:
                    if position in constraints.positional_requirements[i].banned:
                        return False

            for letter in self.letter_counts:
                if constraints.letter_counts[letter][0] > self.letter_counts[letter] or constraints.letter_counts[letter][1] < self.letter_counts[letter]:
                    return False

            return True

        except KeyError:
            return False




class WordBank:
    def __init__(self, words: list[str]) -> None:
        self.bank = [Word(word) for word in words]

    @classmethod
    def load_from_file(cls, path='/usr/share/dict/words') -> WordBank:
        with open(path) as f:
            return cls([word.upper() for word in f.read().splitlines()])

    def find_valid_words(self, constraints: Constraints) -> list[str]:
        valid_words = []

        for word in self.bank:
            if word.is_valid(constraints):
                valid_words.append(word)

        return valid_words






def main():
    bank = WordBank.load_from_file()
    constraints = Constraints(5)
    # constraints.letter_counts['Y'] = [2, 2]
    constraints.positional_requirements[2].required = 'A'
    valid_words = bank.find_valid_words(constraints)
    for word in valid_words:
        print(word)




main()
