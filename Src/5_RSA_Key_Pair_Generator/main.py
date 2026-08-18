from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import sys

def generate_keypair(key_size=2048):
    """
    Generate an RSA key pair.
    Public exponent is conventionally 65537.
    Returns (private_key, public_key) objects.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_private_key(private_key, path, password=None):
    """
    Serialize private_key to PEM (PKCS8) and write it to `path`.
    - If password is provided, use BestAvailableEncryption(password.encode())
    - If not, use NoEncryption()

    TODO: build encryption_algorithm based on password, then call
    private_key.private_bytes(encoding=..., format=..., encryption_algorithm=...)
    and write the resulting bytes to `path` in 'wb' mode.
    """
    if password:
        encryption_algorithm = serialization.BestAvailableEncryption(password.encode())
    else:
        encryption_algorithm = serialization.NoEncryption()

    pem_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm
    )

    with open(path, 'wb') as f:
        f.write(pem_bytes)


def save_public_key(public_key, path):
    """
    Serialize public_key to PEM and write it to `path`.
    - encoding=serialization.Encoding.PEM
    - format=serialization.PublicFormat.SubjectPublicKeyInfo
    - no encryption_algorithm needed (public keys aren't secret)

    TODO: call public_key.public_bytes(...) and write to `path` in 'wb' mode.
    """
    pem_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(path, 'wb') as f:
        f.write(pem_bytes)


def load_private_key(path, password=None):
    """
    Load a private key back from a PEM file.

    TODO: open `path` in 'rb' mode, read the bytes, then call
    serialization.load_pem_private_key(data, password=password.encode() if password else None)
    Return the loaded private key object.
    """
    with open(path, 'rb') as f:
        data = f.read()

    private_key = serialization.load_pem_private_key(
        data,
        password=password.encode() if password else None
    )

    return private_key



def load_public_key(path):
    """
    Load a public key back from a PEM file.

    TODO: open `path` in 'rb' mode, read the bytes, then call
    serialization.load_pem_public_key(data)
    Return the loaded public key object.
    """
    with open(path, 'rb') as f:
        data = f.read()

    public_key = serialization.load_pem_public_key(data)

    return public_key


def get_key_details(private_key):
    """
    Extract human-readable details from a private key for display.
    
    TODO: use private_key.private_numbers() to get p, q, d, and
    .public_numbers.n / .public_numbers.e
    Also use private_key.key_size for the bit length.
    Return a dict, e.g.:
    {
        "key_size": ...,
        "n": ...,
        "e": ...,
        "d": ...,
    }
    """
    numbers = private_key.private_numbers()

    return {
        "key_size": private_key.key_size,
        "n": numbers.public_numbers.n,
        "e": numbers.public_numbers.e,
        "d": numbers.d,
    }



def main():
    """
    Wire it together: generate a keypair, save it, and show its details.
    """
    
    # 1. Ask user for key size
    try:
        key_size_input = input("Key size (1024/2048/4096) [default 2048]: ").strip()
        key_size = int(key_size_input) if key_size_input else 2048

    except ValueError as e:
        print("Please enter the numeric value. \nError: ", e)
        sys.exit()

    # 2. Ask user for an optional password
    password = input("Password to encrypt private key (leave blank for none): ").strip()
    password = password if password else None

    # 3. Generate the keypair
    private_key, public_key = generate_keypair(key_size)

    # 4. Save both keys to disk
    save_private_key(private_key, "private_key.pem", password=password)
    save_public_key(public_key, "public_key.pem")

    # 5. Extract and display details
    details = get_key_details(private_key)
    print("\n--- Key Details ---")
    print(f"Key size: {details['key_size']} bits")
    print(f"n (modulus): {details['n']}")
    print(f"e (public exponent): {details['e']}")
    print(f"d (private exponent): {details['d']}")
    print(f"\nSaved to private_key.pem and public_key.pem")




if __name__ == "__main__":
    main()