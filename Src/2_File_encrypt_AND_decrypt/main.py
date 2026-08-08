from cryptography.fernet import Fernet, InvalidToken
import os
import time
import sys


def generate_key(keypath="secret.key"):
    try:    
        print("Generating Key...........")
        time.sleep(3)
        key = Fernet.generate_key()
        with open (keypath, "wb") as f:
            f.write(key)

        print("\n      Success!")
        print(f"Key Saved to '{keypath}' file")
        print("---------------------------------------------------------------------")

    except OSError as e:

        print("Error! Error! Error!  ",e)

def load_key(keypath = "secret.key"):
    try:
        print("Loading Key........")
        time.sleep(3)
        
        with open (keypath, 'rb') as f:
            return f.read()

    except OSError as e:
        print("Error! Error! Error! ", e)
        sys.exit()


def encrypt_file(file, key):
    
    # 1. Open and read the file in binary mode
    try:
        with open (file, 'rb') as f:
            original_data = f.read()
        

        try:
            print("Encrypting.......")
            time.sleep(3)
        # 2. Create a Fernet object using the key
            fernet = Fernet(key)
            # 3. Call the method that encrypts data
            encrypted_data = fernet.encrypt(original_data)
            
            # 4. Write the result to a new file (decide the naming convention yourself)
            base, ext = os.path.splitext(file)
            new_file_name = base + ".enc"

            
            with open(new_file_name, "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)
            print("\n---------------------------------------------------------------------")
            print(f"          Success! Success! Success!       \nEncryption completed: Data saved in '{new_file_name}' file.")
            print("---------------------------------------------------------------------")

        except ValueError as e:
            print("Error! Error! Error!   Invalid or currupted key file.\n", e)       

    except OSError as e:
        print("Error! Error! Error! ",e)

def decrypt_file(file, key):
    
    #Read the encrypted file in binary
    try:    
        with open(file, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()


        #Decrypt the encrypted data
        try:
            print("Decrypting.........")
            time.sleep(3)
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)

            # Remove _encrypted.enc from the original file and add '_decrypted.dec' as an extention
            base, ext = os.path.splitext(file)
            new_file_name = base + ".dec"

            # Save decrypted data to the file
            with open(new_file_name, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)      

                 
            print("\n---------------------------------------------------------------------")
            print(f"          Success! Success! Success!      \nDecryption completed: Data saved in '{new_file_name}' file.")
            print("---------------------------------------------------------------------")

        except ValueError as e:
                print("Error! Error! Error!   Invalid or currupted key file.\n", e)       

        except InvalidToken as e:
            print("Error! Error! Error!   Decryption failed — wrong key or corrupted file.", e)
            
    except OSError as e:
        print("Error! Error! Error! ",e)






if __name__ == "__main__":
    
    try:
        if len(sys.argv) < 2:
            print("Usage: python main.py [ genkey 'G'|encrypt 'E' |decrypt 'D' ] [Filename]")
            sys.exit(1)

        # print("------------------------------------------------------------------")
        # print("------------------------- FILE CRYPTO ----------------------------")
        # print("------------------------------------------------------------------")
        action = sys.argv[1]
        #file = sys.argv[2]

        if (action == "genkey") or (action == "G"):
                
            print("------------------------- KEY GENERATION ----------------------------\n")  
            generate_key()

        elif (action == "encrypt") or (action == "E"):
            print("---------------------------------------------------------------------")
            print("------------------------- FILE ENCRYPTION ----------------------------\n")            
            key = load_key()
            encrypt_file(sys.argv[2],key)

        elif (action == "decrypt") or (action == "D"):
            print("---------------------------------------------------------------------")
            print("------------------------- FILE DECRYPTION----------------------------\n")  
            key = load_key()
            decrypt_file(sys.argv[2], key)


        else:
            print("Please! Give proper inputs and command.")

    except IndexError as e:
        print(f"Error: {e}. Check if you forgot ot give argument!\nUsage: python main.py [ genkey 'G'|encrypt 'E' |decrypt 'D' ] [Filename]" )    