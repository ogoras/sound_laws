import sys
from phoneme_inv import PhonemeInventory

class GraphemeInventory:
    def __init__(self, notation = "PIE"):
        self.notation = notation
        self.phonemes = PhonemeInventory(notation) # creates empty phoneme inventory
        self.dict = {}
        self.inverse_dict = {}
        self.special_symbols = {}
        self.inverse_special = {}
        # open file notation.graphemes with Unicode support
        with open(notation + ".graphemes", "r", encoding = "utf-8") as f:
            for line in f:
                if line[0] == '#':
                    continue
                words = line.split()
                if len(words) == 0:
                    continue
                self.add(words[0], words[1:])
                
    def add(self, grapheme, qualities):
        # setting the default values
        consonant = True
        accented = False
        syllabic = False
        phoneme_qualities = []
        if "symbol" in qualities:
            # find index of "symbol" in qualities
            index = qualities.index("symbol")
            # and delete
            del qualities[index]
            if len(qualities) != 1:
                print("Error: symbol must have exactly one quality")
                sys.exit(1)
            quality = qualities[0]
            self.special_symbols[grapheme] = quality
            self.inverse_special[quality] = grapheme
            return
        for quality in qualities:
            if quality == "vowel":
                consonant = False
                syllabic = True
            elif quality == "accented":
                accented = True
            elif quality == "syllabic":
                syllabic = True
            else:
                phoneme_qualities.append(quality)
        if consonant:
            phoneme = self.phonemes.add_consonant(grapheme, phoneme_qualities)
        else:
            phoneme = self.phonemes.add_vowel(grapheme, phoneme_qualities)
        grapheme_information = PhonemicGrapheme(phoneme, syllabic, accented)
        self.dict[grapheme] = grapheme_information
        self.inverse_dict[grapheme_information] = grapheme

    def is_syllabic(self, grapheme):
        return self.dict[grapheme].syllabic
    
    def get_phoneme(self, grapheme):
        return self.dict[grapheme].phoneme
    
    def find(self, phoneme, syllabic, accented = False):
        grapheme_information = PhonemicGrapheme(phoneme, syllabic, accented)
        if not grapheme_information in self.inverse_dict:
            print("Error: phoneme not found in inventory: " + phoneme)
            sys.exit(1)
        return self.inverse_dict[grapheme_information]
    
    def find_special(self, quality):
        if not quality in self.inverse_special:
            print("Error: quality not found in inventory: " + quality)
            print(self.special_symbols, self.inverse_special)
            sys.exit(1)
        return self.inverse_special[quality]

class PhonemicGrapheme:
    def __init__(self, phoneme, syllabic, accented):
        self.phoneme = phoneme
        self.syllabic = syllabic
        self.accented = accented

    def __eq__(self, other):
        return self.phoneme == other.phoneme and self.syllabic == other.syllabic and self.accented == other.accented
    def __hash__(self):
        return hash((self.phoneme, self.syllabic, self.accented))