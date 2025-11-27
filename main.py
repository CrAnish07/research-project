import argparse
from secret_scheme import CryptoLayer, BitCombinations

def parse_args():
    parser = argparse.ArgumentParser(description="Secret sharing using k,n,m parameters")

    parser.add_argument("-k", type=int, required=True, help="threshold k (must satisfy n > k > m)")
    parser.add_argument("-n", type=int, required=True, help="number of shares n")
    parser.add_argument("-m", type=int, required=True, help="lower bound m")

    args = parser.parse_args()

    # Validate inequality n > k > m
    if not (args.n > args.k > args.m):
        parser.error("Invalid relation: must satisfy n > k > m")

    return args

def main():
    args = parse_args()

    original_message = "this is my super hey hey hey secret message"

    crypto = CryptoLayer()
    M_prime = crypto.build_secret_for_sharing(original_message)
    print("M' (for sharing):", M_prime)

    combo = BitCombinations(k=5, n=7, m=3, sec_txt=M_prime)
    combo.share_generation()

    reconstructed_M_prime = combo.reconstruct_secret()
    print("\nReconstructed M':", reconstructed_M_prime)

    # Ensure bit-perfect recovery at this layer
    if M_prime != reconstructed_M_prime:
        print("\n[WARNING] M' and reconstructed M' differ!")
    else:
        print("\n[OK] M' reconstructed exactly.")

    recovered_message = crypto.recover_message_from_secret(reconstructed_M_prime)
    print("\nRecovered original message:", recovered_message)


if __name__ == "__main__":
    main()
