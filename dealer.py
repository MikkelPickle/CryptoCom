import random
from common import Triple
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
    
    def user_independent_preprocessing(self):
        a_shares, b_shares, c_shares = self.randmul()
        c = self.open_shares(c_shares)
        c_inv = mod_inverse(c, self.p)
        assert gcd(c, self.p) == 1, f"c and p are not coprime: gcd(c, p) = {gcd(c, self.p)}"
        assert c != 0, "c must not be zero"
        self.k_inverse = a_shares
        self.k = self.convert_secrets_to_curve_representation(b_shares, c_inv)

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
        
    def convert_secrets_to_curve_representation(self, b, c):
        c_inv = mod_inverse(c, self.p)
        k_shares = [self.convert_secret_to_point(share) * c_inv for share in b]
        self.k = k_shares
        return k_shares

    def output(self):
        return self.k, self.k_inverse

        