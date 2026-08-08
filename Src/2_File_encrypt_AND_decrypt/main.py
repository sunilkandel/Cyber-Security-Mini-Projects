from cryptography.fernet import Fernet, InvalidToken
import os
import sys


def generate_key(keypath="secret.key"):
    try:    
        key = Fernet.generate_key()
        with open (keypath, "wb") as f:
            f.write(key)

        print(f"Key Saved to {keypath}")

    except OSError as e:
        print("Error! Error! Error!  ",e)

def load_key(keypath = "secret.key"):
    try:
        with open (keypath, 'rb') as f:
            return f.read()

    except OSError as e:
        print("Error! Error! Error! ", e)
        sys.exit()


def encrypt_file(file, key):
    # TODO:
    # 1. Open and read the file in binary mode
    try:
        with open (file, 'rb') as f:
            original_data = f.read()
        

        try:
        # 2. Create a Fernet object using the key
            fernet = Fernet(key)
            # 3. Call the method that encrypts data
            encrypted_data = fernet.encrypt(original_data)
            
            # 4. Write the result to a new file (decide the naming convention yourself)
            base, ext = os.path.splitext(file)
            new_file_name = base + ".enc"

            
            with open(new_file_name, "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)

        except ValueError as e:
            print("Error! Error! Error!   Invalid or currupted key file.\n", e)       

    except FileNotFoundError as e:
        print("Error! Error! Error! ",e)

def decrypt_file(file, key):
    # TODO: same shape, reversed
    

    
    #Read the encrypted file in binary
    try:    
        with open(file, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()


        #Decrypt the encrypted data
        try:
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            # Remove _encrypted.enc from the original file and add '_decrypted.dec' as an extention
            base, ext = os.path.splitext(file)
            new_file_name = base + ".dec"

            # Save decrypted data to the file
            with open(new_file_name, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)       

        except ValueError as e:
                print("Error! Error! Error!   Invalid or currupted key file.\n", e)       

        except InvalidToken as e:
            print("Error! Error! Error!   Decryption failed — wrong key or corrupted file.", e)
            
    except FileNotFoundError as e:
        print("Error! Error! Error! ",e)






if __name__ == "__main__":
    
    try:
        if len(sys.argv) < 2:
            print("Usage: python main.py [ genkey 'G'|encrypt 'E' |decrypt 'D' ] [Filename]")
            sys.exit(1)

        action = sys.argv[1]
        #file = sys.argv[2]

        if (action == "genkey") or (action == "G"):
            generate_key()

        elif (action == "encrypt") or (action == "E"):
            key = load_key()
            encrypt_file(sys.argv[2],key)

        elif (action == "decrypt") or (action == "D"):
            key = load_key()
            decrypt_file(sys.argv[2], key)


        else:
            print("Please! Give proper inputs and command.")

    except IndexError as e:
        print(f"Error: {e}. Check if you forgot ot give argument!\nUsage: python main.py [ genkey 'G'|encrypt 'E' |decrypt 'D' ] [Filename]" )    