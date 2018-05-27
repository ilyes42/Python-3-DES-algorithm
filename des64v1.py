def cipher(in64bits, key56bits):
    keys = list(genKeys(key56bits))
    x = permute_func(in64bits, ip)
    for i in range(15):
        x = round_func(x, keys[i], True)
    x = round_func(x, keys[15], False)
    x = permute_func(x, fp)
    return x

def reverse_cipher(in64bits, key56bits):
    keys = list(genKeys(key56bits))
    x = permute_func(in64bits, ip)
    for i in range(15, 0, -1):
        x = round_func(x, keys[i], True)
    x = round_func(x, keys[0], False)
    x = permute_func(x, fp)
    return x

# function to be used for the initial and final permutations:


def permute_func(input_64bits, permutationTable):
    output_64bits = []
    for i in range(64):
        output_64bits.append(input_64bits[permutationTable[i]])
    return output_64bits

# function to be used for each of the 16 rounds:


def round_func(input_64bits, key_48bits, swap):
    left = input_64bits[:32]
    right = input_64bits[32:]
    r1 = des_func(right, key_48bits)
    r2 = xor_func(32, r1, left)
    if swap == True:
        return right + r2
    else:
        return r2 + right

# the DES_function:


def des_func(input_32bits, key_48bits):
    # expand the 32bits input into 48bits via d_boxes:
    expanded_input = []
    for i in range(48):
        expanded_input.append(input_32bits[d_box[i]])
    r1 = xor_func(48, expanded_input, key_48bits)
    # go back to 32bits using s-boxes now:
    r2 = []
    for i in range(8):
        six = r1[i*6:(i+1)*6]
        row = int(str(six[0]) + str(six[5]), 2)
        col = int(str(six[1]) + str(six[2]) + str(six[3]) + str(six[4]), 2)
        x = s_box[i][row*16 + col]
        r2 += [int(n) for n in list('{0:04b}'.format(x))]

    r3 = []
    for i in range(32):
        r3.append(r2[d32[i]])

    return r3

# XOR function:


def xor_func(size, bit_list1, bit_list2):
    result = []
    for i in range(size):
        if bit_list1[i] == bit_list2[i]:
            result.append(0)
        else:
            result.append(1)
    return result

# key generation function:


def genKeys(key_56bit):
    left = key_56bit[:28]
    right = key_56bit[28:]
    for i in range(16):
        left = shiftLeft(left, shift_tab[i])
        right = shiftLeft(right, shift_tab[i])
        r1 = left + right
        r2 = []
        for j in range(48):
            r2.append(r1[comp_d_box[j]])
        yield r2


# shiftLeft function:
def shiftLeft(bit_list, n):
    l = [str(x) for x in bit_list]
    b = ''.join(l)
    b = int(b, 2)
    b <<= n
    b = '{0:028b}'.format(b)
    b = [int(e) for e in list(b)]
    return b


# initial permutation:
ip = [57, 49, 41, 33, 25, 17, 9,  1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7,
      56, 48, 40, 32, 24, 16, 8,  0,
      58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6]

# final permutation:
fp = [39,  7, 47, 15, 55, 23, 63, 31,
      38,  6, 46, 14, 54, 22, 62, 30,
      37,  5, 45, 13, 53, 21, 61, 29,
      36,  4, 44, 12, 52, 20, 60, 28,
      35,  3, 43, 11, 51, 19, 59, 27,
      34,  2, 42, 10, 50, 18, 58, 26,
      33,  1, 41,  9, 49, 17, 57, 25,
      32,  0, 40,  8, 48, 16, 56, 24]

# expansion D-box:
d_box = [31,  0,  1,  2,  3,  4,
         3,  4,  5,  6,  7,  8,
         7,  8,  9, 10, 11, 12,
         11, 12, 13, 14, 15, 16,
         15, 16, 17, 18, 19, 20,
         19, 20, 21, 22, 23, 24,
         23, 24, 25, 26, 27, 28,
         27, 28, 29, 30, 31,  0]
# the 8 S-boxes:
s_box = [
    # S1
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

    # S2
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

    # S3
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

    # S4
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

    # S5
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

    # S6
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

    # S7
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

    # S8
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]

# straight 32:
d32 = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30,
       9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]

# shift table:
shift_tab = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# compression d_box:
comp_d_box = [13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3, 25, 7, 15, 6, 26, 19, 12, 1, 40, 51, 30, 36, 46, 54, 29, 39,
              50, 44, 32, 47, 43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31]



# transform a string into bit list:
def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


# get string from bit list:
def frombits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
