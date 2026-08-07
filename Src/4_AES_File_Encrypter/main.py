import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def generate_key():
    # AES-256 key = 32 random bytes
    # TODO: generate and return it
    pass

def encrypt_file(filepath, key):
    # TODO:
    # 1. Read the file in binary
    # 2. Generate a random 16-byte IV
    # 3. Pad the data (block size = 128 bits for AES)
    # 4. Create Cipher(algorithms.AES(key), modes.CBC(iv))
    # 5. Get an encryptor, call .update() + .finalize()
    # 6. Decide: write IV + ciphertext together, or IV separately?
    #    Write the result to a new file
    pass

def decrypt_file(filepath, key):
    # TODO: reverse of the above
    # 1. Read the file, extract the IV (wherever you stored it)
    # 2. Create Cipher with same key + that IV
    # 3. Decrypt, then UNPAD the result (important — don't forget this step)
    # 4. Write the decrypted output
    pass