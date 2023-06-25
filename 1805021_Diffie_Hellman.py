import random
import math

miller_rabin_rounds = 30

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



def generateLargePrime(k):
    while True:
        n = random.randint(2**(k-1), 2**k - 1)
        if n % 2 == 0:
            n += 1  # Make sure n is odd

        if millerRabinTest(n, miller_rabin_rounds):
            return n
        
def findGenerator(p):
    if not millerRabinTest(p, miller_rabin_rounds):
        return None

    factors = []
    phi = p - 1
    n = phi

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            while n % i == 0:
                n //= i

    if n > 1:
        factors.append(n)

    for g in range(2, p):
        is_generator = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                is_generator = False
                break

        if is_generator:
            return g

    return None

print(findGenerator(7))
