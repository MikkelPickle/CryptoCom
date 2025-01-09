from dealer import Dealer
from ecpy.curves import Curve
from bob import Bob
from alice import Alice
from common import verify_signature

def main():
    message = "Claudio is the best"
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
    k_a, k_inv_a = alice.output1()
    k_b, k_inv_b = bob.output1()
    #dependent preprocessing
    alice_u, alice_v, alice_w, bob_u, bob_v, bob_w = dealer.randmul() 
    alice.set_secret_key_share(alice_key_share)
    bob.set_secret_key_share(bob_key_share)
    d_A, e_A = alice.compute_d_and_e(alice_u, alice_v)
    d_B, e_B = bob.compute_d_and_e(bob_u, bob_v)
    alice.open_d_and_e_share(d_A, e_A, d_B, e_B)
    bob.open_d_and_e_share(d_A, e_A, d_B, e_B)
    alice.compute_key_share_prime(alice_w)
    bob.compute_key_share_prime(bob_w)
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
    pub_key_bob = bob.open_point_share_pub_key(alice_pub_key_share)
    print(verify_signature(curve, alice_sig, alice.R.x, pub_key_alice, message))
    print(verify_signature(curve, bob_sig, bob.R.x, pub_key_bob, message))

if __name__ == '__main__':
    main()