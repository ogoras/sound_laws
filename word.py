import sys
from grapheme_inv import GraphemeInventory

syllable_symbol = 'n̥'[1]
PIEsecondary_symbols = ['ʰ', 'ʷ', '₁', '₂', '₃', syllable_symbol]

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
                #vowelInventory = phonemeInventory.vowels
                self.graphemes = graphemes = extractPIEgraphemes(text)
                self.silent_graphemes = [False] * len(self.graphemes)
                self.phonemes = phonemes = [graphemeInventory.get_phoneme(g) for g in graphemes]
                self.length = length = len(phonemes)
                self.syllabic = [graphemeInventory.is_syllabic(s) for s in graphemes]
                self.accented = [graphemeInventory.is_accented(s) for s in graphemes]
                # include sonorants *ey, *oy, *em, *om etc. as syllabic / _C or _#
                for i in range(1, length):
                    if phonemeInventory.is_vowel(phonemes[i-1]) and \
                    consonantInventory.is_sonorant(phonemes[i]):
                        if i == length - 1 or not self.syllabic[i+1]:
                            self.make_syllabic(i)
                # all interconsonantal laryngeals are syllabic (but it's not usually written so we have to check for it)
                for i in range(length):
                    if consonantInventory.check_PoA(phonemes[i], "laryngeal"):
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
        j = self._grapheme_index(i)
        self.graphemes[j] = graphemeInventories[notation].find(symbol, self.syllabic[i], self.accented[i])
        self._update_text()

    def delete_phoneme(self, i):
        # find the grapheme to delete using silent_graphemes
        j = self._grapheme_index(i)
        del self.phonemes[i]
        del self.syllabic[i]
        del self.graphemes[j]
        del self.silent_graphemes[j]
        self.length -= 1
        self._update_text()

    def _update_text(self):
        self.text = "".join(self.graphemes)

    def _grapheme_index(self, phonemeIndex):
        j = 0
        while phonemeIndex > 0:
            j += 1
            if not self.silent_graphemes[j]:
                phonemeIndex -= 1
        return j

    def add_acute(self, i): # i points to the main vowel
        if i < self.length - 1 and not self.syllabic[i+1]:
            PBSvowels = graphemeInventories["PBS"].phonemes.vowels
            PIEvowels = graphemeInventories["PIE"].phonemes.vowels
            phoneme = self.get_phoneme(i)
            if phoneme in ['e', 'o']:
                self.set_phoneme(i, PIEvowels.lengthen(phoneme), "PIE")
            else:
                j = self._grapheme_index(i)
                self.set_phoneme(i, PBSvowels.lengthen(self.graphemes[j]), "PBS")
        # find the end of the nucleus
        while i < self.length and self.syllabic[i]:
            i += 1
        # insert the acute at i and shift the rest of the word
        self.add_special(i, graphemeInventories["PBS"].find_special("acute"))

    def add_special(self, i, special_symbol):
        self.graphemes.insert(i, special_symbol)
        self.silent_graphemes.insert(i, True)
        self._update_text()
        
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