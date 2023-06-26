import random
import math

miller_rabin_rounds = 15

def millerRabinTest(n, k):
    if n <= 1 or n == 4:
        return False  # 0, 1, and even numbers are not prime
    
    if n <= 3:
        return True  # 2 and 3 are prime numbers
    
    # Finding s and d such that n - 1 = 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    
    for _ in range(k):
        a = random.randint(2, n - 2)  # Random base in the range (2, n - 2)
        x = pow(a, d, n)  # Compute a^d mod n
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(s - 1):
            x = pow(x, 2, n)  # Compute x^2 mod n
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    
    return True



# def generateLargePrime(k):
#     i = 1
#     while True:
#         n = random.randint(2**(k-1), 2**k - 1)
#         # n = 2**(k) + i
#         if n % 2 == 0:
#             n += 1  # Make sure n is odd

#         if millerRabinTest(n, miller_rabin_rounds):
#             return n
        
#         i += 2


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


def test(p):
    factors = []
    phi = p - 1
    n = phi

    # factors = pollards_rho(n)
    factors.append(2)
    factors.append(n//2)

    # if n > 1:
    #     factors.append(n)

    print("factors done!!!!!")

    for g in range(2, p):
        is_generator = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                is_generator = False
                break

        if is_generator:
            return g

    return None



def findGeneratorInRange(p, min, max):
    factors = []
    phi = p - 1
    n = phi

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            while n % i == 0:
                n //= i
        # print("done for i:", i)

    if n > 1:
        factors.append(n)

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


# k = int(input("Enter the value of k: "))
# large_prime = generateLargePrime(k)
# print("Large prime:", large_prime)

# mn, mx = map(int, input("Enter the values of min and max separated by a space: ").split())
# while not validateMinMax(mn, mx, large_prime):
#     print("Invalid range. Try again.")
#     mn, mx = map(int, input("Enter the values of min and max separated by a space: ").split())

# primitive_root = findGeneratorInRange(large_prime, mn, mx)

# a = generateLargePrime(k/2)
# b = generateLargePrime(k/2)

# A = modularExponentiation(primitive_root, a, large_prime)
# B = modularExponentiation(primitive_root, b, large_prime)
# print("A:", A, "and B:", B, "are equal:", A == B)

print(test((generateLargePrime(128))))
