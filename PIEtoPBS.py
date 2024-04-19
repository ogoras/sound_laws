# take an input word from the first argument
import sys

syllable_symbol = 'n̥'[1]
PIEsecondary_symbols = ['ʰ', 'ʷ', '₁', '₂', '₃', syllable_symbol]

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

class GraphemeInventory:
    def __init__(self, notation = "PIE"):
        self.notation = notation
        self.phonemes = PhonemeInventory(notation) # creates empty phoneme inventory
        self.dict = {}
        self.inverse_dict = {}
        self.special_symbols = []
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
            self.special_symbols.append(grapheme)
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
    
class PhonemicGrapheme:
    def __init__(self, phoneme, syllabic, accented):
        self.phoneme = phoneme
        self.syllabic = syllabic
        self.accented = accented

    def __eq__(self, other):
        return self.phoneme == other.phoneme and self.syllabic == other.syllabic and self.accented == other.accented
    def __hash__(self):
        return hash((self.phoneme, self.syllabic, self.accented))

graphemeInventories = {
    "PIE": GraphemeInventory("PIE"),
    "PBS": GraphemeInventory("PBS")
}

class Word:
    def __init__(self, text, notation = "PIE"):
        self.text = text
        self.notation = notation
        match notation:
            case "PIE":
                graphemeInventory = graphemeInventories[notation]
                phonemeInventory = graphemeInventory.phonemes
                consonantInventory = phonemeInventory.consonants
                vowelInventory = phonemeInventory.vowels
                self.graphemes = graphemes = extractPIEgraphemes(text)
                self.phonemes = phonemes = [graphemeInventory.get_phoneme(g) for g in graphemes]
                length = len(graphemes)
                self.syllabic = [graphemeInventory.is_syllabic(s) for s in graphemes]
                # include sonorants *ey, *oy, *em, *om etc. as syllabic / _C or _#
                for i in range(1, length):
                    if phonemeInventory.is_vowel(phonemes[i-1]) and \
                    consonantInventory.is_sonorant(phonemes[i]):
                        if i == length - 1 or not self.syllabic[i+1]:
                            self.make_syllabic(i)
                # all interconsonantal laryngeals are syllabic (but it's not usually written so we have to check for it)
                for i in range(length):
                    if consonantInventory.check_PoA(graphemes[i], "laryngeal"):
                        surrounded = False
                        if i > 1:
                            if not self.syllabic[i-1]:
                                surrounded = True
                            else: continue
                        if i < length - 1:
                            if not self.syllabic[i+1]:
                                surrounded = True
                            else: continue
                        if surrounded:
                            self.make_syllabic(i)
            case "PBS":
                # to be implemented
                pass

    def __repr__(self):
        return self.text
    
    def make_syllabic(self, i):
        self.syllabic[i] = True

    def get_phoneme(self, i):
        return self.phonemes[i]
    
    def set_phoneme(self, i, symbol, notation):
        self.phonemes[i] = symbol
        if self.notation != None and notation != self.notation:
            self.notation = None # no biggie
        self.graphemes[i] = graphemeInventories[notation].find(symbol, self.syllabic[i])
        self.text = "".join(self.graphemes)
        
def extractPIEgraphemes(word):
    graphemes = []
    i = 0
    while i < len(word):
        if word[i] in PIEsecondary_symbols:
            if len(graphemes) == 0:
                print("Error: secondary grapheme at beginning of word")
                sys.exit(1)
            graphemes[-1] += word[i]
        else:
            graphemes.append(word[i])
        i += 1
    return graphemes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <word>")
        sys.exit(1)
    text = sys.argv[1]

    # split the word into phones
    word = Word(text, "PIE")
    print("Graphemes:", word.graphemes)
    print("Phonemes:", word.phonemes)
    print("Syllabic:", [1 if s else 0 for s in word.syllabic])

    print(0, word, "Original PIE")

    # apply the RUKI sound law
    # s > š / {r, w, K, y}_
    RUKI = ['r', 'w', 'k', 'g', 'gʰ', 'y']
    consonantInventory = graphemeInventories["PIE"].phonemes.consonants
    for i in range(len(word.graphemes) - 1):
        if word.get_phoneme(i+1) == 's' and consonantInventory.devoice(word.get_phoneme(i)) in RUKI:
            word.set_phoneme(i+1, 'š', "PBS")

    print(1, word, "After RUKI sound law")

    # H > ∅ / C_C in non-initial syllables