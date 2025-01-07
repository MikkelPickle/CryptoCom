from common import hash_to_Zp
from sympy import mod_inverse
from ecpy.curves import Curve,Point

class Alice:
    def __init__(self, curve_order, a, b, c):
        self.curve_order = curve_order
        self.curve = Curve.get_curve('secp256k1')
        self.k_inv = a
        self.b = b
        self.c_share = c

    def compute_key_share_prime(self, key_share):
        self.key_share_prime = (key_share * self.k_inv) % self.curve_order

    def output1(self):
        return self.k, self.k_inv

    def output2(self):
        return self.k, self.k_inv, self.key_share_prime

    def open_point_share(self, point):
        self.R = self.k + point

    def open_c_share(self, c):
        self.c = (self.c_share + c) % self.curve_order

    def convert_secret_to_point(self):
        G = self.curve.generator
        point = self.b * G  
        c_inv = mod_inverse(self.c, self.curve_order)
        self.k = point * c_inv

    def convert_secret_to_point_pub_key(self, secret):
        G = self.curve.generator
        point = secret * G  
        self.pub_key_share = point
        return point

    def open_point_share_pub_key(self, pub_key_share):
        return self.pub_key_share + pub_key_share

    def compute_shared_signature(self, message):
        message_hash = hash_to_Zp(message)
        sig = ((self.k_inv * message_hash) + (self.R.x * self.key_share_prime)) % self.curve_order
        self.sig = sig
        return sig

    def open_sig_share(self, sig):
        return (self.sig + sig) % self.curve_order