# take an input word from the first argument
import sys

syllable_symbol = 'n̥'[1]
PIEsecondary_symbols = ['ʰ', 'ʷ', '₁', '₂', '₃', syllable_symbol]

PIEvowels = ['e', 'ē', 'o', 'ō']
PIEvowel_lengths = [1, 2, 1, 2, 1, 1]
PIEvowel_heights = [3, 3, 3, 3, 6, 6] # 0 = open, 3 = mid, 6 = close
PIEvowel_backness = [0, 0, 2, 2, 0, 2] # 0 = front, 1 = central, 2 = back
PIEvowels_accented = ['é', 'ḗ', 'ó', 'ṓ']

PIEnasals = ['m', 'n']
PIEnasals_PoA = [0, 1] # 0 - labial, 1 - coronal, 2 - palatal, 3 - velar, 4 - labiovelar, 5 - laryngeal
PIEvoiceless_stops = ['p', 't', 'ḱ', 'k', 'kʷ']
PIEvoiced_stops = ['d', 'ǵ', 'g', 'gʷ']
PIEaspirated_stops = ['bʰ', 'dʰ', 'ǵʰ', 'gʰ', 'gʷʰ']
PIEvoiceless_stops_PoA = PIEvoiced_stops_PoA = PIEaspirated_stops_PoA = [0, 1, 2, 3, 4, 5]
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
PIE_MoA = [0, 1, 1, 1, 2, 3, 4, 5] # 0 - nasal, 1 - stop, 2 - fricative, 3 - lateral, 4 - trill, 5 - semivowel
PIEconsonants_phonation = [1, 0, 1, 2, 0, 0, 0, 0] # 0 - voiceless, 1 - voiced, 2 - aspirated voiced

class Word:
    def __init__(self, syllables):
        self.syllables = syllables

class Syllable:
    def __init__(self, onset, nucleus, coda):
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda

class Nucleus:
    def __init__(self, phonemes, accent = 0):
        self.phonemes = phonemes
        self.length = sum([phoneme.length() for phoneme in phonemes])
        self.accent = accent

class Phoneme:
    def __init__(self, symbol, notation = "PIE"):
        match notation:
            case "PIE":
                if symbol in PIEvowels:
                    self.vowel = True
                    self = Vowel(symbol, notation)
                else:
                    self.vowel = False
                    self = Consonant(symbol, notation)
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
                    print("Error: invalid vowel symbol: " + symbol + " (notation: " + notation + ")")
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
                i = 0
                while i < len(PIEconsonants):
                    try:
                        index = PIEconsonants[i].index(symbol)
                    except ValueError:
                        i += 1
                        continue
                    self.MoA = PIE_MoA[i] # manner of articulation
                    self.PoA = PIEconsonants_PoA[i][index] # place of articulation
                    self.phonation = PIEconsonants_phonation[i]
                    return
                print("Error: invalid consonant symbol: " + symbol + " (notation: " + notation + ")")
                sys.exit(1)
            case "PBS":
                # to be implemented
                pass

class Symbol: # in this case symbol = phoneme & sometimes prosodic information
    def __init__(self, symbol, notation = "PIE"):
        self.symbol = symbol
        self.notation = notation
        match notation:
            case "PIE":
                self.syllabic = False
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
                self.phoneme = Phoneme(symbol, notation)
                if self.phoneme.vowel:
                    self.syllabic = True
            case "PBS":
                # to be implemented
                pass

    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return self.symbol
        
        
def analyze(text):
    # split the word into phones
    symbols = extractPIEsymbols(text)
    # identify syllabic phonemes
    syllabic = [s.syllabic for s in symbols]
    clusters = []   # clusters of phonemes, alternating consonant clusters and syllable nuclei]
    in_nucleus = syllabic[0]
    cluster = []
    for i in range(len(symbols)):
        if syllabic[i] == in_nucleus:
            cluster.append(symbols[i])
        else:
            clusters.append(cluster)
            cluster = [symbols[i]]
            in_nucleus = not in_nucleus
    clusters.append(cluster)
    return clusters

def extractPIEsymbols(word):
    symbols = []
    i = 0
    while i < len(word):
        if word[i] in PIEsecondary_symbols:
            if len(symbols) == 0:
                print("Error: secondary symbol at beginning of word")
                sys.exit(1)
            symbols[-1] += word[i]
        else:
            symbols.append(word[i])
        i += 1
    return [Symbol(s, "PIE") for s in symbols]

if len(sys.argv) < 2:
    print("Usage: python PIEtoPBS.py <word>")
    sys.exit(1)
text = sys.argv[1]

# split the word into phones
word = analyze(text)
print(word)

print(0, text, "Original PIE")

# # apply the RUKI sound law
# # s > š / {r, w, K, y}_
# RUKI = ['r', 'w', 'k', 'g', 'gʰ', 'y']
# for i in range(len(phones) - 1):
#     if phones[i + 1] == 's' and phones[i] in RUKI:
#         phones[i+1] = 'š'
# word = ''.join(phones)
# print(1, word, "After RUKI sound law")

# # H > ∅ / C_C in non-initial syllables