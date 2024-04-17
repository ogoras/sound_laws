# take an input word from the first argument
import sys

syllable_symbol = 'n̥'[1]
PIEsecondary_graphemes = ['ʰ', 'ʷ', '₁', '₂', '₃', syllable_symbol]

PIEvowels = ['e', 'ē', 'o', 'ō']
PIEvowel_lengths = [1, 2, 1, 2, 1, 1]
PIEvowel_heights = [3, 3, 3, 3, 6, 6] # 0 = open, 3 = mid, 6 = close
OPEN = 0
MID = 3
CLOSE = 6
PIEvowel_backness = [0, 0, 2, 2, 0, 2] # 0 = front, 1 = central, 2 = back
FRONT = 0
CENTRAL = 1
BACK = 2
PIEvowels_accented = ['é', 'ḗ', 'ó', 'ṓ']

PIEnasals = ['m', 'n']
PIEnasals_PoA = [0, 1] # 0 - labial, 1 - coronal, 2 - palatal, 3 - velar, 4 - labiovelar, 5 - laryngeal
LABIAL = 0
CORONAL = 1
PALATAL = 2
VELAR = 3
LABIOVELAR = 4
LARYNGEAL = 5
PIEvoiceless_stops = ['p', 't', 'ḱ', 'k', 'kʷ']
PIEvoiced_stops = ['d', 'ǵ', 'g', 'gʷ']
PIEaspirated_stops = ['bʰ', 'dʰ', 'ǵʰ', 'gʰ', 'gʷʰ']
PIEvoiceless_stops_PoA = PIEaspirated_stops_PoA = [0, 1, 2, 3, 4]
PIEvoiced_stops_PoA = [1, 2, 3, 4]
PIEfricatives = ['s', 'h₁', 'h₂', 'h₃']
PIEfricatives_PoA = [1, 5, 5, 5]
PIElaterals = ['l']
PIElaterals_PoA = [1]
PIEtrills = ['r']
PIEtrills_PoA = [1]
PIEsemivowels = ['y', 'w']
PIEsemivowels_PoA = [2, 4]
PIEconsonants = [PIEnasals, PIEvoiceless_stops, PIEvoiced_stops, PIEaspirated_stops, PIEfricatives, PIElaterals, PIEtrills, PIEsemivowels]
PIEconsonants_PoA = [PIEnasals_PoA, PIEvoiceless_stops_PoA, PIEvoiced_stops_PoA, PIEaspirated_stops_PoA, PIEfricatives_PoA, PIElaterals_PoA, PIEtrills_PoA, PIEsemivowels_PoA]
PIEconsonants_MoA = [0, 1, 1, 1, 2, 3, 4, 5] # 0 - nasal, 1 - stop, 2 - fricative, 3 - lateral, 4 - trill, 5 - semivowel
NASAL = 0
STOP = 1
FRICATIVE = 2
LATERAL = 3
TRILL = 4
SEMIVOWEL = 5
SONORANT = [NASAL, LATERAL, TRILL, SEMIVOWEL]
PIEconsonants_phonation = [1, 0, 1, 2, 0, 0, 0, 0] # 0 - voiceless, 1 - voiced, 2 - aspirated voiced
VOICELESS = 0
VOICED = 1
ASPIRATED_VOICED = 2

class Word:
    def __init__(self, text, notation = "PIE"):
        self.text = text
        self.notation = notation
        match notation:
            case "PIE":
                self.graphemes = graphemes = extractPIEgraphemes(text)
                self.syllabic = [s.syllabic for s in graphemes]
                # include sonorants *ey, *oy, *em, *om etc. as syllabic / _C or _#
                for i in range(1, len(graphemes)):
                    if graphemes[i-1].phoneme.vowel and not graphemes[i].phoneme.vowel and graphemes[i].phoneme.MoA in SONORANT:
                        if i == len(graphemes) - 1 or not self.syllabic[i+1]:
                            self.make_syllabic(i)
                # all interconsonantal laryngeals are syllabic (but it's not usually written so we have to check for it)
                for i in range(len(graphemes)):
                    if not graphemes[i].phoneme.vowel and graphemes[i].phoneme.PoA == LARYNGEAL:
                        surrounded = False
                        if i > 1:
                            if not self.syllabic[i-1]:
                                surrounded = True
                            else: continue
                        if i < len(graphemes) - 1:
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
        self.graphemes[i].syllabic = True

    def get_phoneme(self, i):
        return self.graphemes[i].phoneme
    
    def set_phoneme(self, i, symbol, notation):
        if self.notation != None and notation != self.notation:
            self.notation = None # no biggie
        grapheme = Grapheme(symbol, notation)
        self.graphemes[i] = grapheme
        self.syllabic[i] = grapheme.syllabic

# class Syllable:
#     def __init__(self, onset, nucleus, coda):
#         self.onset = onset
#         self.nucleus = nucleus
#         self.coda = coda

# class Nucleus:
#     def __init__(self, phonemes, accent = 0):
#         self.phonemes = phonemes
#         self.length = sum([phoneme.length() for phoneme in phonemes])
#         self.accent = accent
            
class Phoneme:
    def devoiced(self):
        return self

    def __repr__(self):
        return self.symbol
    
    def __eq__(self, other):
        return isinstance(other, Phoneme) and self.symbol == other.symbol

def phoneme(grapheme, notation = "PIE"):
    match notation:
        case "PIE":
            if grapheme in PIEvowels:
                return Vowel(grapheme, notation)
            else:
                return Consonant(grapheme, notation)
        case "PBS":
            # to be implemented
            pass

class Vowel(Phoneme):
    def __init__(self, symbol, notation):
        self.vowel = True
        self.symbol = symbol
        self.notation = notation
        self.phonation = 1 # assumption true for all IE languages
        match notation:
            case "PIE":
                # find the index in the PIEvowels list
                try:
                    index = PIEvowels.index(symbol)
                except ValueError:
                    print("Error: invalid vowel grapheme: " + symbol + " (notation: " + notation + ")")
                    sys.exit(1)
                self.length = PIEvowel_lengths[index]
                self.height = PIEvowel_heights[index]
                self.backness = PIEvowel_backness[index]
            case "PBS":
                # to be implemented
                pass

class Consonant(Phoneme):
    def __init__(self, symbol, notation):
        self.vowel = False
        self.symbol = symbol
        self.notation = notation
        match notation:
            case "PIE":
                for i in range(len(PIEconsonants)):
                    try:
                        index = PIEconsonants[i].index(symbol)
                    except ValueError:
                        continue
                    self.MoA = PIEconsonants_MoA[i] # manner of articulation
                    self.PoA = PIEconsonants_PoA[i][index] # place of articulation
                    self.phonation = PIEconsonants_phonation[i]
                    return
                print("Error: invalid consonant symbol: " + symbol + " (notation: " + notation + ")")
                sys.exit(1)
            case "PBS":
                # to be implemented
                pass

    def devoiced(self):
        if self.phonation == VOICELESS:
            return self
        devoiced = Consonant.from_qualities(self.MoA, self.PoA, VOICELESS, self.notation)
        if devoiced == None:
            return self
        else:
            return devoiced
        
    def from_qualities(MoA, PoA, phonation, notation):
        match notation:
            case "PIE":
                for i in range(len(PIEconsonants)):
                    if PIEconsonants_MoA[i] != MoA or PIEconsonants_phonation[i] != phonation:
                        continue
                    for j in range(len(PIEconsonants[i])):
                        if PIEconsonants_PoA[i][j] == PoA:
                            return Consonant(PIEconsonants[i][j], notation)
                return None
            

class Grapheme: # in this case represents phoneme & sometimes prosodic information
    def __init__(self, symbol, notation = "PIE"):
        self.grapheme = symbol
        self.notation = notation
        match notation:
            case "PIE":
                self.syllabic = False
                symbol = symbol
                index = -1
                try:
                    index = PIEvowels_accented.index(symbol)
                except ValueError:
                    pass
                if index != -1:
                    self.accented = True
                    symbol = PIEvowels[index]
                elif symbol[-1] == syllable_symbol:
                    self.syllabic = True
                    symbol = symbol[:-1]
                elif symbol == 'i':
                    self.syllabic = True
                    symbol = 'y'
                elif symbol == 'u':
                    self.syllabic = True
                    symbol = 'w'
                self.phoneme = phoneme(symbol, notation)
                if self.phoneme.vowel:
                    self.syllabic = True
            case "PBS":
                # to be implemented
                pass

    def __str__(self):
        return self.grapheme
    
    def __repr__(self):
        return self.grapheme
        
def extractPIEgraphemes(word):
    graphemes = []
    i = 0
    while i < len(word):
        if word[i] in PIEsecondary_graphemes:
            if len(graphemes) == 0:
                print("Error: secondary grapheme at beginning of word")
                sys.exit(1)
            graphemes[-1] += word[i]
        else:
            graphemes.append(word[i])
        i += 1
    return [Grapheme(s, "PIE") for s in graphemes]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python PIEtoPBS.py <word>")
        sys.exit(1)
    text = sys.argv[1]

    # split the word into phones
    word = Word(text, "PIE")
    print("Graphemes:", word.graphemes)
    print("Phonemes:", [s.phoneme for s in word.graphemes])
    print("Syllabic:", [1 if s else 0 for s in word.syllabic])

    print(0, word, "Original PIE")

    # apply the RUKI sound law
    # s > š / {r, w, K, y}_
    RUKI = ['r', 'w', 'k', 'g', 'gʰ', 'y']
    RUKI = [phoneme(symbol, "PIE") for symbol in RUKI]
    for i in range(len(word.graphemes) - 1):
        if word.get_phoneme(i+1) == phoneme('s', "PIE") and word.get_phoneme(i).devoiced() in RUKI:
            word.set_phoneme(i+1, 'š', "PBS")

    print(1, word, "After RUKI sound law")

    # # H > ∅ / C_C in non-initial syllables