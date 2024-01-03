class PositionalRequirements {
    required: string;
    banned: string[];

    constructor() {
        this.required: '';
        this.banned = [];
    }
}

class Constraints {
    letterCounts { [key: string] : number[]};
    positionalRequirements: PositionalRequirements[];
    length: number;

    constructor(length: number) {
         this.letterCounts = {};
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split('').forEach(letter => {
            this.letterCounts[letter] = [0, 5];
        });
        this.positionalRequirements = Array.from({ length }, () => new PositionalRequirements());
        this.length = length;

    }
}

}

class Word {
    positional: string[];
    letterCounts: { [key: string]: number };

    constructor(word: string) {
        this.positional = Array.from(word);
        this.letterCounts = {};
        word.split('').forEach(letter => {
            this.letterCounts[letter] = (this.letterCounts[letter] || 0) + 1;
        });
    }

    isValid(constraints: Constraints): boolean {
        if (constraints.length !== this.positional.length) {
            return false;
        }

        for (let i = 0; i < this.positional.length; i++) {
            const position = this.positional[i];
            const req = constraints.positionalRequirements[i];

            if (req.required && req.required !== position) {
                return false;
            } else if (req.banned.includes(position)) {
                return false;
            }
        }

        for (const letter in constraints.letterCounts) {
            if (constraints.letterCounts[letter][0] > (this.letterCounts[letter] || 0)) {
                return false;
            }

            if (constraints.letterCounts[letter][1] < (this.letterCounts[letter] || 0)) {
                return false;
            }
        }
        return true;
    }
}

class WordBank {
    bank: Word[];

    constructor(words: string[]) {
        this.bank = words.map(word => new Word(word));
    }


    findValidWords(constraints: Constraints): string[] {
        return this.bank.filter(word => word.isValid(constraints)).map(word => word.toString());
    }
}
