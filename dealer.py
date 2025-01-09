import random
from ecpy.curves import Curve,Point
from sympy import mod_inverse
from math import gcd

class Dealer:
    def __init__(self, curve):
        self.p = curve.order
        self.curve = curve
        self.secret = None
        self.k = None
        self.k_inverse = None

    def generate_key(self):
        secret = random.randint(0, self.p - 1)
        self.secret = secret
        return secret

    def randmul(self):
        a = random.randint(1, self.p - 1)
        b = random.randint(1, self.p - 1)
        c = (a * b) % self.p

        alice_a, bob_a = self.secret_share(a)
        alice_b, bob_b = self.secret_share(b)
        alice_c, bob_c = self.secret_share(c)

        return alice_a, alice_b, alice_c, bob_a, bob_b, bob_c

    def secret_share(self, value):
        share_alice = random.randint(0, self.p - 1)
        share_bob = (value - share_alice) % self.p
        assert (share_alice + share_bob) % self.p == value, f"Share mismatch: {(share_alice + share_bob) % self.p} != {value}"
        return share_alice, share_bob

        