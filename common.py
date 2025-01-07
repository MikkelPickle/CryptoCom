from hashlib import sha256
from sympy import mod_inverse

class Triple:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

def hash_to_Zp(message):
    curve_order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    message_hash = sha256(message.encode()).digest()
    hash_int = int.from_bytes(message_hash, byteorder='big') % curve_order
    return hash_int

def verify_signature(curve, sig, rx, P, message):
    G = curve.generator
    curve_order = curve.order
    w = mod_inverse(sig, curve_order)
    H_m = hash_to_Zp(message)
    u1 = (H_m * w) % curve_order
    u2 = (rx * w) % curve_order
    R_prime = (u1 * G) + (u2 * P)
    return (R_prime.x % curve_order) == rx




