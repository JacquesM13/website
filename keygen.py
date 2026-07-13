from sympy import primerange
import random

# ---- Select two Prime Numbers:  P and Q ----
P = int(input("Provide a prime number: "))
Q = int(input("Provide another: "))


# ---- Calculate the Product: P * Q ----
N = P * Q


# ---- Calculate the Totient of N: (P-1) * (Q-1) ----
T = (P-1) * (Q-1)
# print(f"Totient: {T}")


# ---- Select a Public Key ----
#   the value which must match three requirements:
#     It must be Prime
#     It must be less than the Totient E < T
#     It must NOT be a factor of the Totient T % E != 0

# Calculate primes up to Totient
x = 2
y = T -1
primes = list(primerange(x, y + 1))

# Remove values which are factors of Totient
for prime in primes[:]:
    if T % prime == 0:
        primes.remove(prime)

# Select public key from remaining primes
E = random.choice(primes)
print(f"--- Public Key: {E}")


# ---- Select a Private Key ----
#   the Product of the Public Key and the Private Key when divided by the Totient, must result in a remainder of 1
#   (D * E) % T = 1
# Select a Private Key
#   the Product of the Public Key and the Private Key when divided by the Totient, must result in a remainder of 1
#   (D * E) % T = 1

nums = list(range(0, 1000))
for num in nums[:]:
    if (num * E) % T != 1:
        nums.remove(num)

D = random.choice(nums)
print(f"--- Private Key: {D}\n")

# ---- Encrypting a number ----

M = int(input("Provide a number to encrypt: "))
C = M**E % N
print(f"Your number after encryption number is: {C}")

O = C**D % N
print(f"After decryption: {O}")