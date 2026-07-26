from cryptography.fernet import Fernet

def generate_key(key_path="secret.key"):
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
    print(f"Key saved to {key_path}")

def load_key(key_path="secret.key"):
    with open(key_path, "rb") as f:
        return f.read()

def encrypt_file(filepath, key):
    # TODO:
    # 1. Read the file in binary mode
    # 2. Create a Fernet object with the key
    # 3. Encrypt the data
    # 4. Write it to filepath + ".enc"
    pass

def decrypt_file(filepath, key):
    # TODO: reverse of encrypt_file
    # careful: what should the output filename be?
    pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python file_crypto.py [genkey|encrypt|decrypt] [filename]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "genkey":
        generate_key()
    elif action == "encrypt":
        key = load_key()
        encrypt_file(sys.argv[2], key)
    elif action == "decrypt":
        key = load_key()
        decrypt_file(sys.argv[2], key)