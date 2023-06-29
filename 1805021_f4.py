import socket
from AES_1805021 import inputValidation, key_scheduling, decrypt 
from Diffie_Hellman_1805021 import generateLargePrime, modularExponentiation, computeSharedKey

def BOB():
    host = "localhost"
    port = 6236

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)

        client_socket, address = s.accept()

        data = client_socket.recv(1024).decode().split(" ")
        # print("Received data", data)
        p = data[0]
        g = data[1]
        A = data[2]
        k  = int(p).bit_length()
        print("Received p, g, and A from Alice:", p, g, A, "OF LENGTH", k)

        p = int(p)
        g = int(g)
        A = int(A)
        b = generateLargePrime(k//2)

        B = modularExponentiation(g, b, p)
        B = str(B)
        print("Generated B:", B)
        client_socket.sendall(B.encode())

        shared_key = computeSharedKey(A, b, p)
        hex_key = str(shared_key).encode("utf-8").hex()
        # print("Generated shared key:", hex_key)

        # client_socket.recv(1024).decode()
        # s.sendall("done".encode())

        cipher_text = client_socket.recv(1024).decode()
        print("Received cipher text from Alice:", cipher_text)

        hex_key = inputValidation("", hex_key, k)[1]
        print("Key after server-side validation:", hex_key)
        key_list = key_scheduling(hex_key, k)
        # print("Generated key list:", key_list[5])

        decipher_text = decrypt(cipher_text, key_list, k)

        print("Decipher Text in HEX:", decipher_text)
        print("Decipher Text in ASCII:", bytearray.fromhex(decipher_text).decode('unicode-escape'))

        s.close()
    
    print("Connection closed")

BOB()
