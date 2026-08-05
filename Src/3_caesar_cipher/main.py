
def caesar_encrypt(text, shift):
    result = ""
    for char in text:

        if char.isupper():
            # TODO: handle uppercase letters
            result += chr((ord(char) + shift - ord("A")) % 26 + ord("A"))

        elif char.islower():
            # TODO: handle lowercase letters
            result += chr((ord(char) + shift - ord('a')) % 26 + ord("a"))

        else:
            # TODO: handle non-alphabet characters (numbers, spaces, punctuation) — leave unchanged
            result += char

    return result



def caesar_decrypt(text, shift):
    # TODO: think about this — do you need new logic,
    # or can you just call caesar_encrypt with a modified shift?
    return caesar_encrypt(text, 0-shift)




if __name__ == "__main__":
    msg = input("Enter your message: ")
    shift = int(input("Enter shift value : "))
    mode = input ("Encrypt or Decrypt? (e/d): ")

    if  mode.lower() == "e" or mode.lower() == "encrypt":
        print("Result: ", caesar_encrypt(msg, shift))

    elif mode.lower() == "d" or mode.lower() == "decrypt":
        print("Result: ", caesar_decrypt(msg, shift))

    else:
        print("Please enter valid mode  Encrypt or Decrypt")