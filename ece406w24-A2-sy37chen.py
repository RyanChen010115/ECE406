#!/usr/bin/env python3
"""
Assignment 2 Python file
Copy-and-paste your extended_euclid and modexp functions
from assignment 1
"""
import random
import math

################################################################################
# student info
#
# WatIAM username: sy37chen 
# Student number: 20830005
################################################################################


# TODO: Add implementations of modexp and extended_euclid (you can resuse your code from A1).
def modexp(x, y, N):
    """
    Input: Three positive integers x and y, and N.
    Output: The number x^y mod N
    """
    if y == 0:
        return 1
    z = modexp(x,y//2,N)
    if y%2:
        return (x*(z**2))%N
    else:
        return (z**2)%N


# part (ii) for extended Euclid  -- fill in the code below
def extended_euclid(a, b):
    """
    Input: Two positive integers a >= b >= 0
    Output: Three integers x, y, and d returned as a tuple (x, y, d)
            such that d = gcd(a, b) and ax + by = d
    """
    if b ==0:
        return 1,0,a
    x,y,d = extended_euclid(b, a%b)
    return y, x-(a//b)*y,d

def primality(N):
    """
    Test if a number N is prime using Fermat's little Theorem with
    ten random values of a.  If a^(N-1) mod N = 1 for all values,
    then return true.  Otherwise return false.
    Hint:  you can generate a random integer between a and b using
    random.randint(a,b).
    """
    # TODO: Implement a True/False test for primality of an input number N.
    for i in range(10):
        a = random.randint(1,N-1)
        if modexp(a,N-1,N) != 1:
            return False
    return True


def prime_generator(N):
    """
    This function generates a prime number <= N
    """
    # TODO: Implement a prime number generator.
    seen = set()
    while len(seen) <= N:
        randomNum = random.randint(1,N)
        if randomNum in seen:
            continue
        seen.add(randomNum)
        if primality(randomNum):
            return randomNum
    return 0


def main():
    """
    Generate RSA private/public key, then encode and decode a message.
    """
    ## A2Q1:  generating primes and RSA
    ##################
    p = 0
    q = 0
    N = 0
    e = 5
    x = 2148321
    key = 0
    while True:
        seen = set()
        p = prime_generator(10000000)
        q = prime_generator(10000000)
        if (p,q) in seen or (q,p) in seen:
            continue
        seen.add((p,q))
        key,a,d = extended_euclid(e,(p-1)*(q-1))
        if d == 1:
            break
    print(f'P: {p}, Q: {q}')
    N = p * q
    if key < 0: #value used for private key
        key += (p-1)*(q-1)
    print(f"Private key: {key}")
    # TODO: Complete this main() function.
    #       You should use print statements to show that your code completes the 
    #       instructions from parts iii--vi.
    encrypted = modexp(x,e,N)
    print(f'Encrypted message: {encrypted}')
    decrypted = modexp(encrypted,key,N)
    print(f'Decrypted message: {decrypted}')
    if decrypted == x:
        print("Success")
    else:
        print("Decrypted message does not match original")
if __name__ == '__main__':
    main()
