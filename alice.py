from common import hash_to_Zp
from sympy import mod_inverse
from ecpy.curves import Curve,Point
import random

class Alice:
    def __init__(self, curve_order, a, b, c):
        self.curve_order = curve_order
        self.curve = Curve.get_curve('secp256k1')
        self.k_inv = a
        self.b = b
        self.c_share = c

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
    
    def set_secret_key_share(self, sk):
        self.key_share = sk

    def compute_d_and_e(self, u, v):
        d_A = (self.key_share + u) % self.curve_order
        e_A = (self.k_inv + v) % self.curve_order
        return d_A, e_A
    
    def open_d_and_e_share(self, d_A, e_A, d_B, e_B):
        self.e = (e_A + e_B) % self.curve_order
        self.d = (d_A + d_B) % self.curve_order
    
    def compute_key_share_prime(self, w):
        self.key_share_prime = (w + self.e*self.key_share + self.d*self.k_inv + self.e*self.d) % self.curve_order

    def open_point_share_pub_key(self, pub_key_share):
        return self.pub_key_share + pub_key_share

    def compute_shared_signature(self, message):
        message_hash = hash_to_Zp(message)
        sig = ((self.k_inv * message_hash) + (self.R.x * self.key_share_prime)) % self.curve_order
        self.sig = sig
        return sig

    def open_sig_share(self, sig):
        return (self.sig + sig) % self.curve_order