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

def checksum_length(wordlist): # in hex characters
    num_bits = len(wordlist)/3
    return int(num_bits/4)

def isValidMnemonic(wordlist):
    bigNum = 0
    n_hex_digit = int(len(wordlist)*11/4)
    for word in wordlist:
        if word not in word_list_bip39:
            print(f"The word '{word}' is not present in the bip 39 wordlist")
            exit() 
        bigNum = (bigNum<<11) + word_list_bip39.index(word)
    # nhex = format(N, '033x') # include leading zero if needed
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

def ElaboraMnemonic(mnemonic_string):
    if isinstance(mnemonic_string, str):
        mnemonic_wordlist = mnemonic_string.lower().strip().split()
    elif isinstance(mnemonic_string, list):
        mnemonic_wordlist = mnemonic_string
    # else:
    #     print("La variabile non è né una stringa né una lista.")    
    if len(mnemonic_wordlist) == 11:
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
