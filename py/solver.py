from __future__ import annotations
from collections import Counter, defaultdict
import string

class PositionalRequirements:
    def __init__(self) -> None:
        self.required = ''
        self.banned = []

    def __str__(self):
        return f"PositionalRequirements: required: {self.required}; banned: {self.banned}"


class Constraints:
    def __init__(self, length: int) -> None:
        self.letter_counts = {letter: [0, 5] for letter in string.ascii_uppercase}
        self.positional_requirements = [PositionalRequirements() for _ in range(length)]
        self.length = length

    def __str__(self):
        return f"Constraints: {self.positional_requirements}; {self.letter_counts}"


class Word:
    def __init__(self, word: str) -> None:
        self.positional = list(word)
        self.letter_counts = defaultdict(int, {letter: count for letter, count in Counter(word).items()})

    def __str__(self):
        return f"{''.join(self.positional)}"

    def is_valid(self, constraints: Constraints) -> bool:
        if constraints.length != len(self.positional):
            return False

        for i, position in enumerate(self.positional):
            if constraints.positional_requirements[i].required and constraints.positional_requirements[i].required != position:
                return False
            else:
                if position in constraints.positional_requirements[i].banned:
                    return False

        for letter in constraints.letter_counts:
            if constraints.letter_counts[letter][0] > self.letter_counts[letter]:
                return False

            if constraints.letter_counts[letter][1] < self.letter_counts[letter]:
                return False

        return True


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

    constraints.letter_counts['A'] = [0, 0]
    constraints.letter_counts['L'] = [1, 5]
    constraints.letter_counts['I'] = [1, 5]
    constraints.letter_counts['E'] = [0, 0]
    constraints.letter_counts['N'] = [0, 0]
    constraints.letter_counts['O'] = [0, 0]
    constraints.letter_counts['S'] = [0, 0]
    constraints.letter_counts['P'] = [0, 0]
    constraints.letter_counts['T'] = [1, 5]
    constraints.letter_counts['R'] = [1, 5]


    constraints.positional_requirements[1].banned.append('L')
    constraints.positional_requirements[2].required = 'I'

    constraints.positional_requirements[3].banned.append('I')
    constraints.positional_requirements[4].required = 'L'

    constraints.positional_requirements[0].required = 'T'
    constraints.positional_requirements[1].banned.append('R')

    words = [Word('BOOKS'), Word('BROKE'), Word('BRAKE'), Word('CROOK'), Word('OAAAO')]




    valid_words = bank.find_valid_words(constraints)
    for word in valid_words:
        print(word)




main()
