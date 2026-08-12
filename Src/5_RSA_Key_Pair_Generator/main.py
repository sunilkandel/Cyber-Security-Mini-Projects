from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


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
    pass


def load_public_key(path):
    """
    Load a public key back from a PEM file.

    TODO: open `path` in 'rb' mode, read the bytes, then call
    serialization.load_pem_public_key(data)
    Return the loaded public key object.
    """
    pass


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
    pass


def main():
    """
    TODO: wire it together —
    1. Ask user for key size (e.g. 1024/2048/4096)
    2. Ask user for an optional password
    3. Call generate_keypair(key_size)
    4. Call save_private_key(...) and save_public_key(...)
    5. Call get_key_details(...) and print/display it
    This is also where you'll later swap in the Tkinter GUI instead of
    plain input()/print() calls.
    """
    pass


if __name__ == "__main__":
    main()