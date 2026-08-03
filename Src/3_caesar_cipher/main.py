
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        # TODO: handle uppercase letters
        # TODO: handle lowercase letters
        # TODO: handle non-alphabet characters (numbers, spaces, punctuation) — leave unchanged
        pass
    return result

def caesar_decrypt(text, shift):
    # TODO: think about this — do you need new logic,
    # or can you just call caesar_encrypt with a modified shift?
    pass



if __name__ == "__main__":
    msg = input("Enter your message: ")
    shift = input("Enter shift value : ")
    mode = input ("Encrypt or Decrypt? (e/d): ")

    if  mode.lower() == "e":
        print("Result: ", caesar_encrypt(msg, shift))

    else:
        print("Result: ", caesar_decrypt(msg, shift))