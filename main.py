from dealer import Dealer
from ecpy.curves import Curve,Point
from bob import Bob
from alice import Alice
from common import verify_signature

def main():
    message = "hej"
    curve = Curve.get_curve('secp256k1')
    dealer = Dealer(curve)
    secret = dealer.generate_key()
    alice_key_share, bob_key_share = dealer.secret_share(secret)
    #independent preprocessing 
    alice_a, alice_b, alice_c, bob_a, bob_b, bob_c = dealer.randmul()
    alice = Alice(curve.order, alice_a, alice_b, alice_c) 
    bob = Bob(curve.order, bob_a, bob_b, bob_c)
    alice.open_c_share(bob_c)
    bob.open_c_share(alice_c)
    alice.convert_secret_to_point()
    bob.convert_secret_to_point()
    alice.output1()
    bob.output1()
    #dependent preprocessing
    a1, b1, c1, a2, b2, c2 = dealer.randmul() #?? 
    alice.compute_key_share_prime(alice_key_share)
    bob.compute_key_share_prime(bob_key_share)
    k_a, k_inv_a, key_share_prime_a = alice.output2()
    k_b, k_inv_b, key_share_prime_b = bob.output2()
    #the signature protocol
    alice.open_point_share(k_b)
    bob.open_point_share(k_a)
    alice_sig_share = alice.compute_shared_signature(message)
    bob_sig_share = bob.compute_shared_signature(message)
    alice_sig = alice.open_sig_share(bob_sig_share)
    bob_sig = bob.open_sig_share(alice_sig_share)
    #verification
    alice_pub_key_share = alice.convert_secret_to_point_pub_key(alice_key_share)
    bob_pub_key_share = bob.convert_secret_to_point_pub_key(bob_key_share)
    pub_key_alice = alice.open_point_share_pub_key(bob_pub_key_share)
    pub_key_bob = alice.open_point_share_pub_key(alice_pub_key_share)
    print(verify_signature(curve, alice_sig, alice.R.x, pub_key_alice, message))

    




if __name__ == '__main__':
    main()