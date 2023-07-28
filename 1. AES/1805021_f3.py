import socket
from AES_1805021 import inputValidation, key_scheduling, encrypt 
from Diffie_Hellman_1805021 import generateLargePrime, findGeneratorInRange, modularExponentiation, computeSharedKey
from Diffie_Hellman_1805021 import mn, mx

# Alice -> Client
def ALICE():
    host = "localhost"
    port = 6236

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        k = int(input("Enter bit length: "))
        p = generateLargePrime(k)
        g = findGeneratorInRange(p, mn[k], mx[k])
        a = generateLargePrime(k//2)
        A = modularExponentiation(g, a, p)

        p = str(p)
        g = str(g)
        A = str(A)
        print("Generated g:", g)
        print("Generated p:", p)
        print("Generated A:", A)

        data = p + " " +  g + " " + A
        s.sendall(data.encode())
        # s.sendall(p.encode())
        # s.sendall(g.encode())

        B = s.recv(1024).decode()
        B = int(B)
        print("Received B from Bob:", B)

        p = int(p)
        shared_key = computeSharedKey(B, a, p)
        hex_key = str(shared_key).encode("utf-8").hex()
        # print("Generated shared key:", hex_key)

        # s.sendall("done".encode())
        # s.recv(1024).decode()

        # AES encryption
        plain_text = input("Enter plain text: ")
        hex_plain_text = plain_text.encode("utf-8").hex()

        hex_plain_text_arr, hex_key = inputValidation(hex_plain_text, hex_key, k)
        print("Key after clinet-side validation:", hex_key)
        key_list = key_scheduling(hex_key, k)
        # print("Generated key list:", key_list[5])

        cipher_text = encrypt(hex_plain_text_arr, key_list, k)
        print("Generated cipher Text in HEX:", cipher_text)

        s.sendall(cipher_text.encode())

        s.close()

    print("Connection closed")


ALICE()
