import random
import math
import time

miller_rabin_rounds = 15
trials = 5
mx = {
    128: 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890,
    192: 12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890,
    256: 12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
}
mn = {
    128: 1234567890,
    192: 12345678901234567890,
    256: 1234567890123456789012345678901234567890
}

def millerRabinTest(n, k):
    if n <= 1 or n == 4:
        return False
    
    if n <= 3:
        return True
    
    # Finding s and d such that n - 1 = 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    
    for _ in range(k):
        a = random.randint(2, n - 2) 
        x = pow(a, d, n)  # a^d mod n
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(s - 1):
            x = pow(x, 2, n)  # x^2 mod n
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    
    return True


def generateLargePrime(k):
    while True:
        q = random.randint(2**(k-1), 2**k-1)
        q |= (1 << k - 1) | 1
        while not millerRabinTest(q, miller_rabin_rounds):
            q = random.randrange(2**(k-1), 2**k)
            q |= (1 << k - 1) | 1
        # print(q)
        n = 2*q + 1
        if millerRabinTest(n, miller_rabin_rounds):
            # print(n)
            return n


def pollards_rho(n):
    if n == 1:
        return []

    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def f(x):
        return (x**2 + 1) % n

    x = 2
    y = 2
    d = 1
    factors = []

    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)

    if d == n:
        # Factorization failed
        return []
    else:
        # Recursively factorize the factors
        factors.extend(pollards_rho(d))
        factors.extend(pollards_rho(n // d))

    return factors


def findGeneratorInRange(p, min, max):
    factors = []
    phi = p - 1
    n = phi

    factors.append(2)
    factors.append(n//2)

    # print("factors done!!!!!")

    for g in range(min, max+1):
        is_generator = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                is_generator = False
                break

        if is_generator:
            return g

    return None


def validateMinMax(min, max, p):
    if min >= p or max >= p or min > max:
        return False

    return True


def modularExponentiation(g, a, p):
    res = 1
    g = g % p

    while a > 0:
        if a % 2 == 1:
            res = (res * g) % p

        a //= 2
        g = (g * g) % p

    return res


def computeSharedKey(A, b, p):
    return modularExponentiation(A, b, p)



if __name__ == "__main__":
    bit_length = [128, 192, 256]

    for k in bit_length:
        time_large_prime_start = 0
        time_large_prime_end = 0
        time_primitive_root_start = 0
        time_primitive_root_end = 0
        time_a_start = 0
        time_a_end = 0
        time_A_start = 0
        time_A_end = 0
        time_shared_key_start = 0
        time_shared_key_end = 0

        for t in range(trials):
            time_large_prime_start += time.time()
            large_prime = generateLargePrime(k)
            time_large_prime_end += time.time()

            min, max = mn[k], mx[k]

            time_primitive_root_start += time.time()
            primitive_root = findGeneratorInRange(large_prime, min, max)
            if(primitive_root == None):
                print("No primitive root found in range", min, "to", max, "for", large_prime)
                continue
            time_primitive_root_end += time.time()

            time_a_start += time.time()
            a = generateLargePrime(k//2)
            time_a_end += time.time()
            b = generateLargePrime(k//2)

            time_A_start += time.time()
            A = modularExponentiation(primitive_root, a, large_prime)
            time_A_end += time.time()
            B = modularExponentiation(primitive_root, b, large_prime)

            time_shared_key_start += time.time()
            s1 = computeSharedKey(A, b, large_prime)
            time_shared_key_end += time.time()
            s2 = computeSharedKey(B, a, large_prime)

        # Time-related performance
        time_large_prime = (time_large_prime_end - time_large_prime_start) / trials
        time_primitive_root = (time_primitive_root_end - time_primitive_root_start) / trials
        time_a = (time_a_end - time_a_start) / trials
        time_A = (time_A_end - time_A_start) / trials
        time_shared_key = (time_shared_key_end - time_shared_key_start) / trials

        print("Bit Length:", k)
        print("Time taken for generating large prime:", time_large_prime, "seconds")
        print("Time taken for finding primitive root:", time_primitive_root, "seconds")
        print("Time taken for generating a:", time_a, "seconds")
        print("Time taken for generating A:", time_A, "seconds")
        print("Time taken for generating shared key:", time_shared_key, "seconds\n")
