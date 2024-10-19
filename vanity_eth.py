from coincurve import PrivateKey
from sha3 import keccak_256
import time
import re


def generate_ethereum_address(private_key=None):
    if private_key is None:
        private_key = PrivateKey()
    public_key = private_key.public_key.format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]
    address = "0x" + addr.hex()
    return address, private_key.to_hex()


def find_custom_address(pattern, prefix=True):

    attempts = 0
    start_time = time.time()
    while True:
        address, private_key = generate_ethereum_address()
        attempts += 1

        if (prefix and address[2:].startswith(pattern)) or (not prefix and address[2:].endswith(pattern)):
            end_time = time.time()
            print(f"Matching address found after {attempts} attempts!")
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            print(f"Address: {address}")
            print(f"Private Key: {private_key}")
            return address, private_key

def get_user_input():
    # Validate the pattern only contains hex characters
    while True:
        pattern = input("Enter the desired pattern (hexadecimal characters, 0-9, a-f): ").lower()
        if re.match(r'^[0-9a-f]+$', pattern):
            break
        else:
            print("Invalid input. Please enter only hexadecimal characters (0-9, a-f).")

    # Choose prefix or suffix by entering '1' or '2'
    while True:
        choice = input("Type '1' for prefix or '2' for suffix: ")
        if choice == '1':
            prefix = True
            break
        elif choice == '2':
            prefix = False
            break
        else:
            print("Invalid choice. Please enter '1' for prefix or '2' for suffix.")

    length = len(pattern)
    if length <= 5:
        print("Simple search: 1-5 characters.")
    elif 6 <= length <= 8:
        print("This is a difficult search: 6-8 characters.")
    else:
        print("This is a very difficult search: 9+ characters, may take a long time.")

    return pattern, prefix


if __name__ == "__main__":
    pattern, prefix = get_user_input()
    find_custom_address(pattern, prefix)
