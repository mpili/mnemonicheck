#!/usr/bin/env python3

"""
Autore: Mauro Pili
Data: 2024-03-25

dall'idea https://bitcan.world/

glyph in ascii code

 -
|X|
 -
|X|
 -

 -
|\|
 -
|/|
 -

 . 
...
 . 
...
 . 

"""

import binascii

CHAR_EMPTY = "."

def has_bit_set(number, bit_position):
    mask = 1 << bit_position
    return (number & mask) != 0

def hline(is_on):
	return CHAR_EMPTY + "-" + CHAR_EMPTY if is_on else CHAR_EMPTY * 3

def vline(is_on):
	return "|" if is_on else CHAR_EMPTY

def slashxbackslash(low, high):
	if low and high:
		return "x"
	if low:
		return "\\"
	if high:
		return "/"
	return CHAR_EMPTY

def pipexpipe(n, b1, b2, b3, b4):
	return vline(has_bit_set(n, b1)) + slashxbackslash(has_bit_set(n, b2), has_bit_set(n, b3)) + vline(has_bit_set(n, b4))
    

def r1(n):
	return hline(has_bit_set(n, 0))

def r2(n):
	return pipexpipe(n, 1, 2, 3, 4)

def r3(n):
	return hline(has_bit_set(n, 5))

def r4(n):
	return pipexpipe(n, 6, 7, 8, 9)

def r5(n):
	return hline(has_bit_set(n, 10))

def bitcan_glyph(n):
	return [
		r1(n),
		r2(n),
		r3(n),
  		r4(n),
		r5(n)
	]

if __name__ == "__main__":
	for i in range(512):
		print(i)
		for s in bitcan_glyph(i):
			print(s)
   