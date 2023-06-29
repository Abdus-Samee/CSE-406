from BitVector import *
import time

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)


def inputValidation(text, key, k):
    # PKCS7 Padding
    l = len(key)
    limit = k//4
    if l < limit:
        r = int((limit-l)/2) # hex digits to pad
        key = key + r*"00"
    elif l >= limit:
        key = key[:limit] # 32 hex characters => 16 bytes => 128 bits

    # print("key:", bytearray.fromhex(key).decode('unicode-escape'))

    l = len(text)
    if l < 32:
        r = int((32-l)/2)
        text_list = [text + r*"00"]
    else:
        text_list = [text[i:i+32] for i in range(0, len(text), 32)]
        last_l = len(text_list[-1])
        if last_l < 32:
            r = int((32-last_l)/2)
            text_list[-1] = text_list[-1] + r*"00"
        
    # printTextList(text_list)

    return text_list, key


def printTextList(l):
    for i in range(len(l)):
        print(bytearray.fromhex(l[i]).decode('unicode-escape'), end=" ")
    print()
    

def g(w, r_c):
    # print("got:", w)
    w = w.get_bitvector_in_hex()
    w = w[2:] + w[:2]
    # print("shifted:", w)
    b_w = BitVector(hexstring=w)
    sub_w = BitVector(size = 0)
    for i in range(4):
        sub_w += BitVector(intVal = Sbox[b_w[i*8:i*8+8].intValue()], size = 8)
    sub_w[0:8] ^= r_c

    # print(sub_w.get_bitvector_in_hex())
    return sub_w


def constructInitStateMat(hex_plain_text):
    state_mat = []
    for i in range(0, 8, 2):
        state_row = []
        for j in range(4):
            state_row.append(BitVector(hexstring = hex_plain_text[i+j*8:i+j*8+2]))
        
        state_mat.append(state_row)
    
    return state_mat


def addRoundKey(state_mat, hex_key):
    round_key_mat = []

    for i in range(0, 8, 2):
        round_key_row = []
        for j in range(4):
            round_key_row.append(BitVector(hexstring=hex_key[i+j*8:i+j*8+2]))
        
        round_key_mat.append(round_key_row)
    
    new_state_mat = []
    for i in range(4):
        new_state_row = []
        for j in range(4):
            new_state_row.append(state_mat[i][j]^round_key_mat[i][j])
        new_state_mat.append(new_state_row)

    return new_state_mat


def substitutionByte(state_mat):
    for i in range(4):
        for j in range(4):
            state_mat[i][j] = BitVector(intVal = Sbox[state_mat[i][j].intValue()], size = 8)

    return state_mat


def inverseSubstitutionByte(state_mat):
    for i in range(4):
        for j in range(4):
            state_mat[i][j] = BitVector(intVal = Sbox.index(state_mat[i][j].intValue()), size = 8)

    return state_mat


def shiftRow(state_mat):
    for i in range(4):
        state_mat[i] = state_mat[i][i:] + state_mat[i][:i]

    return state_mat


def inverseShiftRow(state_mat):
    for i in range(4):
        state_mat[i] = state_mat[i][-i:] + state_mat[i][:-i]

    return state_mat


def mixColumn(state_mat):
    fixed_mat = [
        [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
        [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
        [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
        [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
    ]

    new_state_mat = []
    for i in range(4):
        new_state_row = []
        for j in range(4):
            new_state_row.append(BitVector(intVal=0, size=8))
        new_state_mat.append(new_state_row)

    for i in range(4):
        for j in range(4):
            for k in range(4):
                prod = fixed_mat[i][k].gf_multiply_modular(state_mat[k][j], BitVector(intVal=0x11b, size=9), 8)
                new_state_mat[i][j] ^= prod

    return new_state_mat


def inverseMixColumn(state_mat):
    fixed_mat = [
        [BitVector(hexstring="0e"), BitVector(hexstring="0b"), BitVector(hexstring="0d"), BitVector(hexstring="09")],
        [BitVector(hexstring="09"), BitVector(hexstring="0e"), BitVector(hexstring="0b"), BitVector(hexstring="0d")],
        [BitVector(hexstring="0d"), BitVector(hexstring="09"), BitVector(hexstring="0e"), BitVector(hexstring="0b")],
        [BitVector(hexstring="0b"), BitVector(hexstring="0d"), BitVector(hexstring="09"), BitVector(hexstring="0e")]
    ]

    new_state_mat = []
    for i in range(4):
        new_state_row = []
        for j in range(4):
            new_state_row.append(BitVector(intVal=0, size=8))
        new_state_mat.append(new_state_row)

    for i in range(4):
        for j in range(4):
            for k in range(4):
                prod = fixed_mat[i][k].gf_multiply_modular(state_mat[k][j], BitVector(intVal=0x11b, size=9), 8)
                new_state_mat[i][j] ^= prod

    return new_state_mat


def AESRound(key_list, round_no, rounds, state_mat, type="encrypt"):
    if type == "encrypt":
        state_mat = substitutionByte(state_mat)
        state_mat = shiftRow(state_mat)
        if round_no != rounds:
            state_mat = mixColumn(state_mat)
    else:
        state_mat = inverseShiftRow(state_mat)
        state_mat = inverseSubstitutionByte(state_mat)
        state_mat = addRoundKey(state_mat, key_list[rounds-round_no])
        if round_no != rounds:
            state_mat = inverseMixColumn(state_mat)

    return state_mat


def readCipherText(state_mat):
    cipher_text = ""
    for j in range(4):
        for i in range(4):
            cipher_text += state_mat[i][j].get_bitvector_in_hex()

    return cipher_text


def key_scheduling(hex_key, k):
    word_group = k//32
    rounds = word_group + 6
    total_words = (rounds+1)*4
    key_words = [None for i in range(total_words)]
    r_c = BitVector(intVal=0x01, size=8)

    for i in range(word_group):
        key_words[i] = BitVector(hexstring=hex_key[i*32:i*32+32])

    for i in range(word_group, total_words):
        temp = key_words[i-1]
        if i % word_group == 0:
            temp = g(temp, r_c)
            key_words[i] = key_words[i-word_group] ^ temp
            r_c = r_c.gf_multiply_modular(BitVector(intVal=0x02, size=8), BitVector(intVal=0x11b, size=9), 8)
        else:
            key_words[i] = key_words[i-word_group] ^ key_words[i-1]

    key_list = []
    for i in range(rounds+1):
        key_list.append((key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3]).get_bitvector_in_hex())

    return key_list


def printMatrix(mat):
    for i in range(4):
        for j in range(4):
            print(mat[i][j].get_bitvector_in_hex(), end=" ")
        print()


def encrypt(hex_plain_text_arr, key_list, k):
    cipher_text = ""
    rounds = k//32 + 6

    for hex_plain_text in hex_plain_text_arr:
        state_mat = constructInitStateMat(hex_plain_text)
        state_mat = addRoundKey(state_mat, key_list[0])

        for i in range(1, rounds+1):
            state_mat = AESRound(key_list, i, rounds, state_mat)
            state_mat = addRoundKey(state_mat, key_list[i])

        cipher_text += readCipherText(state_mat)

    return cipher_text


def decrypt(cipher_text, key_list, k):
    cipher_text_arr = [cipher_text[i:i+32] for i in range(0, len(cipher_text), 32)]

    decipher_text = ""
    for cipher_text in cipher_text_arr:
        i = k//32 + 6
        rounds = k//32 + 6
        state_mat = constructInitStateMat(cipher_text)
        state_mat = addRoundKey(state_mat, key_list[i])

        for j in range(1, rounds+1):
            state_mat = AESRound(key_list, j, rounds, state_mat, "decrypt")
            i -= 1

        decipher_text += readCipherText(state_mat)

    return decipher_text



if __name__ == "__main__":
    k = 128
    # k = 192
    # k = 256
    print("Enter plain text:")
    plain_text = input()
    print("Enter key:")
    key = input()
    hex_plain_text = plain_text.encode("utf-8").hex()
    hex_key = key.encode("utf-8").hex()

    print("\nPlain Text:")
    print("In ASCII:", plain_text)
    print("In HEX:", hex_plain_text)
    print("\nKey:")
    print("In ASCII:", key)
    print("In HEX:", hex_key)
    print()

    # Input Validation
    hex_plain_text_arr, hex_key = inputValidation(hex_plain_text, hex_key, k)

    # Key Scheduling
    key_start = time.time()
    key_list = key_scheduling(hex_key, k)
    key_end = time.time()

    ## Encryption
    enc_start = time.time()
    cipher_text = encrypt(hex_plain_text_arr, key_list, k)
    enc_end = time.time()
    print("Cipher Text:")
    print("In Hex:", cipher_text)
    print("In ASCII:", bytearray.fromhex(cipher_text).decode('unicode-escape'))
    print()

    #Decryption
    dec_start = time.time()
    decipher_text = decrypt(cipher_text, key_list, k)
    dec_end = time.time()
    print("Deciphered Text:")
    print("In Hex:", decipher_text)
    print("In ASCII:", bytearray.fromhex(decipher_text).decode('unicode-escape'))
    print()

    ## Computation Time
    print("Execution time details:")
    print("Key Scheduling :", (key_end-key_start), "seconds")
    print("Encryption Time:", (enc_end-enc_start), "seconds")
    print("Decryption Time:", (dec_end-dec_start), "seconds")
