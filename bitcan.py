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

# CHAR_EMPTY = " "
# CHAR_VLINE = "|"
# CHAR_HLINE = "-"
# CHAR_SLASH = "/"
# CHAR_BACKSLASH = "\\"
# CHAR_CROSS = "X"
# CHAR_BOX = "O"

CHAR_EMPTY = " "
CHAR_VLINE = "┃"
CHAR_HLINE = "━"
CHAR_SLASH = "╱"
CHAR_BACKSLASH = "╲"
CHAR_CROSS = "╳"
CHAR_BOX = "΃" 

def has_bit_set(number, bit_position):
    mask = 1 << bit_position
    return (number & mask) != 0

def hline(is_on):
	return CHAR_EMPTY + CHAR_HLINE + CHAR_EMPTY if is_on else CHAR_EMPTY * 3

def vline(is_on):
	return CHAR_VLINE if is_on else CHAR_EMPTY

def slashxbackslash(low, high):
	if low and high:
		return CHAR_CROSS
	if low:
		return CHAR_BACKSLASH
	if high:
		return CHAR_SLASH
	return CHAR_BOX

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

def bitcan_glyph_array(n_list):
	# array_risultati = map(bitcan_glyph, n_list)
	rows = []
	matrice_glifi = [bitcan_glyph(n) for n in n_list]
	for i in range(5):
		r = ""
		for g in matrice_glifi:
			r = r + g[i] + "   "	
		rows.append(r) # append the string r
	return rows

def print_bitcan_glyph_array(n_list):
	for r in bitcan_glyph_array(n_list):
		print(r)

def test_n_list():
	n_list = [
    	0b11010010011,
		0b00111011000,
		0b10010100111,
		0b11101000000,
  		0b10001100010,
    	0b00001111110,
     	0b10011001011,
      	0b01110110101,
		0b11110110011,
		0b11101101000,
		0b10110001110,
		0b00000000011
    ]
	print_bitcan_glyph_array(n_list)

if __name__ == "__main__":
	test_n_list()