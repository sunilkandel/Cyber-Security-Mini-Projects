from cryptography.fernet import Fernet


def generate_key(keypath="secret.key"):
    key = Fernet.generate_key()
    with open (keypath, "wb") as f:
        f.write(key)

    print(f"Key Saved to {keypath}")

def load_key(keypath = "secret.key"):
    with open (keypath, 'rb') as f:
        return f.read()



def encrypt_file(file, key):
    # TODO:
    # 1. Open and read the file in binary mode
    with open (file, 'rb') as f:
        original_data = f.read()

    # 2. Create a Fernet object using the key
    fernet = Fernet(key)

    # 3. Call the method that encrypts data
    encrypted_data = fernet.encrypt(original_data)
    
    # 4. Write the result to a new file (decide the naming convention yourself)
    new_file_name = file.replace(".txt", "_encrypted.enc")
    with open(new_file_name, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)


def decrypt_file(file, key):
    # TODO: same shape, reversed
    fernet = Fernet(key)

    
    #Read the encrypted file in binary
    with open(file, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()


    #Decrypt the encrypted data
    decrypted_data = fernet.decrypt(encrypted_data)

    # Remove .enc from the original file and add '_decrypted.txt' as an extention
    original_file_name = file.replace("_encrypted.enc", "_decrypted.dnc")

    # Save decrypted data to the file
    with open(original_file_name, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py [ genkey 'G'|encrypt 'E' |decrypt 'D' ] [Filename]")
        sys.exit(1)

    action = sys.argv[1]
    #file = sys.argv[2]

    if (action == "genkey") | (action == "G"):
        generate_key()

    elif (action == "encrypt") | (action == "E"):
        file = sys.argv[2]
        key = load_key()
        encrypt_file(file,key)

    if (action == "genkey") | (action == "D"):
        file = sys.argv[2]
        key = load_key()
        decrypt_file(file, key)


    