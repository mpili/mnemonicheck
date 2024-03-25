#!/usr/bin/env python3

"""
Autore: Mauro Pili
Data: 2024-03-21
"""

import argparse
import hashlib
import binascii

word_list_file ="wordlist/english.txt"
word_list_index = {}
def carica_wordlist() -> list:
    word_list = open(word_list_file).read().splitlines()
    for i in range(len(word_list)):
        word_list_index[word_list[i]] = i
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
        if x in word_list_bip39:
            return word_list_index[x]
        raise ValueError(f"'{x}' is not a valid mnemonic word")
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


def isValidMnemonic(wordlist):
    bigNum = 0
    n_hex_digit = int(len(wordlist)*11/4)
    for word in wordlist:
        check_word_present_in_bip39(word)
        index = word_list_index[word] 
        # bigNum = (bigNum<<11) + word_list_bip39.index(word)
        bigNum = (bigNum<<11) + index
    # print(bigNum)
    nhex = format(bigNum, f'0{n_hex_digit}x') # include leading zero if needed
    # print(nhex)
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

def ElaboraMnemonic(mnemonic_string):
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
        print("valid" if isValidMnemonic(mnemonic_wordlist) else "non valid")

def main(args):
    if args.file:
        try:
            with open(args.file, "r") as f:
                ElaboraMnemonic(f.read())
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
    # Se è stata specificata una lista di parole
    elif args.lista:
        ElaboraMnemonic(args.lista)
    else:
        ElaboraMnemonic(input("Enter the 12 or 11 mnemonic words: "))


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Analysis validity mnemonic list or search for the 12th valid word")

  # Argomento opzionale: file
  parser.add_argument("-f", "--file", help="Name of file with the 12 or 11 mnemonic words")

  # Argomento opzionale: lista di parole
  parser.add_argument("-l", "--lista", nargs='+', help="list of the mnemonic words")
  
  main(parser.parse_args())
