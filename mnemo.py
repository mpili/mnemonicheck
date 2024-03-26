#!/usr/bin/env python3

"""
Autore: Mauro Pili
Data: 2024-03-21
"""

import argparse
import hashlib
import binascii

import bitcan

HELP_EXAMPLES = """
Examples:
mnemo.py -f file_with_11_or_12_words.txt

# -l with 11 words
mnemo.py -l abandon ability able about above absent absorb abstract absurd abuse access ability

# -l with 12 words
mnemo.py -l abandon ability able about above absent absorb abstract absurd abuse access

# -l with binary value
mnemo.py -l 10010010001

# -l with binary values
mnemo.py -l 11010010011 00111011000 10010100111 11101000000 10001100010 00001111110 10011001011 01110110101 11110110011 11101101000 10110001110 00000000011

# -i enter interactively
mnemo.py -i

# -g show bitcan.world glyph
mnemo.py -g -l YOUTH SOLAR ABANDON COVER URGE TERM LOUD ENGAGE ALL SLOT ABOVE ACCIDENT

"""

word_list_file ="wordlist/english.txt"
word_list_index = {}
def carica_wordlist() -> list:
    word_list = open(word_list_file).read().splitlines()
    for i in range(len(word_list)):
        word_list_index[word_list[i].lower()] = i
    return word_list

word_list_bip39 = carica_wordlist()

def containsonly01(stringa):
  """
  Verifica se una stringa contiene solo 0 e 1.

  Parametri:
    stringa: la stringa da controllare.

  Restituisce:
    True se la stringa contiene solo 0 e 1, False altrimenti.
  """
  for carattere in stringa:
    if carattere not in "01":
      return False
  return True
def bin_dec_word(word):
    index = word_list_index[word]
    return f"{format(index, '011b')} {str(index).rjust(4)} {word}"

def ToNum(x): # accetta binario, decimale o word bip39, restituisce il numero
    if isinstance(x, str):
        if containsonly01(x):
            return int(x, 2)
        w = x.lower()
        if w in word_list_bip39:
            return word_list_index[w]
        raise ValueError(f"{x} is not a valid mnemonic word")
    if isinstance(x, int):
        return x
    raise ValueError(f"'{x}' is not a valid value")

def check_word_present_in_bip39(word):
    """Checks if a word is present in the BIP-0039 English word list"""
    if word not in word_list_bip39:
        raise ValueError(f"'{word}' is not present in the BIP-0039 word list")

def printMnemonic(wordlist):
    for i in range(len(wordlist)):
        x = wordlist[i]
        n = ToNum(x)
        if n < len(word_list_bip39):
            print(f"{format(n, '011b')} {str(n).rjust(4)} {word_list_bip39[n]}")
        else:
            print(f"{format(n, '011b')} {x}")
            # print(f"{str(i+1).rjust(2)} {word_list_bip39[n]}")

def checksum_length(wordlist): # in hex characters
    num_bits = len(wordlist)/3
    return int(num_bits/4)

def BigNum(wordlist): # in hex characters
    bigNum = 0
    for word in wordlist:
        bigNum = (bigNum<<11) + ToNum(word)
    return bigNum

def isValidMnemonic(wordlist):
    n_hex_digit = int(len(wordlist)*11/4)
    bigNum = BigNum(wordlist)
    nhex = format(bigNum, f'0{n_hex_digit}x') # include leading zero if needed
    h = hashlib.sha256(binascii.unhexlify(nhex[:-checksum_length(wordlist)])).hexdigest()
    return h[0] == nhex[-1]

def findTwelfthWords(wordlist): # trova le 12° parole valide 
    n=0
    for word in word_list_bip39:
        new_wordlist = wordlist.copy()
        new_wordlist.append(word)
        if isValidMnemonic(new_wordlist):
            n = n+1
            print(n, ' '.join(new_wordlist))

def dropChecksum(word): # converte la parola in binario, rimuove il checksum, restituisce la parola senza il checksum
    v12th = ToNum(word)
    binstr = format(v12th, '011b')
    l = 4 # checksum_length
    return binstr[0:-l]

def findChecksum(wordlist):
    w12th = dropChecksum(wordlist[11])
    for word in word_list_bip39:
        if dropChecksum(word) == w12th:
            new_wordlist = wordlist.copy()
            new_wordlist[11] = word
            if isValidMnemonic(new_wordlist):
                print(' '.join(new_wordlist))

def ElaboraMnemonic(mnemonic_string, args):
    if isinstance(mnemonic_string, str):
        mnemonic_wordlist = mnemonic_string.lower().strip().split()
    elif isinstance(mnemonic_string, list):
        mnemonic_wordlist = mnemonic_string
    # else:
    #     print("La variabile non è né una stringa né una lista.")
    printMnemonic(mnemonic_wordlist)
    if len(mnemonic_wordlist) == 1:
        pass
    elif len(mnemonic_wordlist) == 11:
        findTwelfthWords(mnemonic_wordlist)
    else:
        if args.checksum:
            findChecksum(mnemonic_wordlist)
        else:
            print("valid" if isValidMnemonic(mnemonic_wordlist) else "non valid")
    if args.glyph:
        bitcan.print_bitcan_glyph_array([ToNum(w) for w in mnemonic_wordlist])

def main(args):
    if args.file:
        try:
            with open(args.file, "r") as f:
                mnemonic_string = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
    # Se è stata specificata una lista di parole
    elif args.lista:
        mnemonic_string = args.lista
    elif args.input:
        mnemonic_string = input("Enter the 12 or 11 mnemonic words: ")
    ElaboraMnemonic(mnemonic_string, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analysis validity mnemonic list or search for the 12th valid word")

    # Argomento obbligatorio: 12 o 11 parole
    # parser.add_argument("wordlist", nargs="+", help="12 or 11 mnemonic words")

    # Argomento opzionale: file
    parser.add_argument("-f", "--file", help="Name of file with the 12 or 11 mnemonic words")

    # Argomento opzionale: lista di parole
    parser.add_argument("-l", "--lista", nargs='+', help="list of the mnemonic words")

    parser.add_argument('-i', '--input', action='store_true', help='enter the words')

    parser.add_argument('-g', '--glyph', action='store_true', help='draw the bitcan glyph')

    parser.add_argument('-c', '--checksum', action='store_true', help='find the checksum in the last word')

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        print(HELP_EXAMPLES)
    else:
        main(args)
