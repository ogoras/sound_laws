# take an input word from the first argument
import sys
from word import Word, graphemeInventories

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
    RUKI = ['r', 'w', 'k', 'y']
    consonantInventory = graphemeInventories["PIE"].phonemes.consonants
    for i in range(word.length - 1):
        if word.get_phoneme(i+1) == 's' and consonantInventory.devoice(word.get_phoneme(i)) in RUKI:
            word.set_phoneme(i+1, 'š', "PBS")

    print(1, word, "After RUKI sound law")

    # H > ∅ / C_C in non-initial syllables