import sys

HEIGHT = {
    "open": 0,
    "mid": 3,
    "close": 6,
    "" : 3 # default value
}
BACKNESS = {
    "front": 0,
    "central": 1,
    "back": 2,
    "" : 1 # default value
}
MoA = {
    "nasal": 0,
    "stop": 1,
    "fricative": 2,
    "lateral": 3,
    "trill": 4,
    "semivowel": 5,
    "" : 2
}
PoA = {
    "labial": 0,
    "coronal": 1,
    "palatal": 2,
    "velar": 3,
    "labiovelar": 4,
    "laryngeal": 5,
    "" : 1
}
SONORANT = ["nasal", "lateral", "trill", "semivowel"]

class PhonemeInventory:
    def __init__(self, notation = "PIE"):
        self.notation = notation
        self.vowels = VowelInventory(notation)
        self.consonants = ConsonantInventory(notation)

    def add_vowel(self, symbol, qualities):
        return self.vowels.add(symbol, qualities)

    def add_consonant(self, symbol, qualities):
        return self.consonants.add(symbol, qualities)
    
    def is_vowel(self, symbol):
        return symbol in self.vowels.dict

class VowelInventory:
    def __init__(self, notation = "PIE"):
        self.notation = notation
        self.dict = {}
        self.inverse_dict = {}

    def add(self, symbol, qualities):
        backness = BACKNESS[""]
        height = HEIGHT[""]
        long = False
        variant = 1
        for quality in qualities:
            if quality in BACKNESS:
                backness = BACKNESS[quality]
            elif quality in HEIGHT:
                height = HEIGHT[quality]
            elif quality == "long":
                long = True
            elif quality == "short":
                long = False
            elif quality.isnumeric():
                variant = int(quality)
            else:
                print("Error: invalid vowel quality: " + quality)
                sys.exit(1)
        vowel = Vowel(backness, height, long, variant)
        self.dict[symbol] = vowel
        if not vowel in self.inverse_dict:
            self.inverse_dict[vowel] = symbol
        return self.inverse_dict[vowel]
    
class Vowel:
    def __init__(self, backness, height, long, variant):
        self.backness = backness
        self.height = height
        self.long = long
        self.variant = variant

    def __eq__(self, other):
        return self.backness == other.backness and \
            self.height == other.height and self.long == other.long and self.variant == other.variant

    def __hash__(self):
        return hash((self.backness, self.height, self.long, self.variant))

class ConsonantInventory:
    def __init__(self, notation = "PIE"):
        self.notation = notation
        self.dict = {}
        self.inverse_dict = {}

    def add(self, symbol, consonant):
        voiced = True
        aspirated = False
        place = PoA[""]
        manner = MoA[""]
        variant = 1
        for quality in consonant:
            if quality == "voiceless" or quality == "voiced":
                voiced = quality == "voiced"
            elif quality == "aspirated" or quality == "unaspirated":
                aspirated = quality == "aspirated"
            elif quality in PoA:
                place = PoA[quality]
            elif quality in MoA:
                manner = MoA[quality]
            elif quality.isnumeric():
                variant = int(quality)
            else:
                print("Error: invalid consonant quality: " + quality)
                sys.exit(1)
        consonant = Consonant(voiced, aspirated, place, manner, variant)
        self.dict[symbol] = consonant
        if not consonant in self.inverse_dict:
            self.inverse_dict[consonant] = symbol
        return self.inverse_dict[consonant]

    def is_sonorant(self, symbol):
        if not symbol in self.dict:
            return False
        return self.dict[symbol].manner in SONORANT

    def check_PoA(self, symbol, place):
        if not symbol in self.dict:
            return False
        return self.dict[symbol].place == PoA[place]
    
    def devoice(self, symbol):
        if not symbol in self.dict:
            return symbol
        consonant = self.dict[symbol]
        consonant.voiced = False
        consonant.aspirated = False
        if consonant in self.inverse_dict:
            return self.inverse_dict[consonant]
        return symbol

class Consonant:
    def __init__(self, voiced, aspirated, place, manner, variant):
        self.voiced = voiced
        self.aspirated = aspirated
        self.place = place
        self.manner = manner
        self.variant = variant

    def __eq__(self, other):
        return self.voiced == other.voiced and \
            self.aspirated == other.aspirated and self.place == other.place and \
            self.manner == other.manner and self.variant == other.variant

    def __hash__(self):
        return hash((self.voiced, self.aspirated, self.place, self.manner, self.variant))