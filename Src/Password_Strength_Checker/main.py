import re

"""Password Strength Checker Using python"""
print()
print("--------------------------------------------------------------------------------------")
print("--------------- P A S S W O R D    S T R E N G T H    C H E C K E R ------------------")
print("--------------------------------------------------------------------------------------")


def password_strength_checker(password):
    score = 0
    feedback = []

    #Character strength checker
    if len(password) >= 8:
        score += 1
        feedback.append(" ✅  Make it at least 8 character long.")
    else:
        feedback.append(" ❌ Make it at least 8 character long.")


    # Check UpperCase
    if (len(re.findall(r'[A-Z]', password))) >=1:
        score += 1
        feedback.append(" ✅  Please enter at least one UpperCase Character. e.g. A B C D ")
    else:
        feedback.append(" ❌ Please enter at least one UpperCase Character. e.g. A B C D ")


    #Check Lowercase
    if (len(re.findall(r'[a-z]', password))) >=1:
        score += 1
        feedback.append(" ✅  Please enter at least one LowerCase Character. e.g. a b c d")
    else:
        feedback.append(" ❌ Please enter at least one LowerCase Character. e.g. a b c d")


    #Check Digits
    if (len(re.findall(r'[0-9]', password))) >=1:
        score += 1
        feedback.append(" ✅  Please enter at least one Numeric Character. e.g. 1234")
    else:
        feedback.append(" ❌ Please enter at least one Numeric Character. e.g. 1234")


    #Check special Character
    if (len(re.findall(r'[^A-Za-z0-9]', password))) >=1:
        score += 1
        feedback.append(" ✅  Please enter at least one Special Character. e.g. !@#$% ")
    else:
        feedback.append(" ❌ Please enter at least one Special Character. e.g. !@#$% ")


    return score, feedback


if __name__ == "__main__":
    
    while True:
        print()
        pwd = input("Enter Your Password: ")
        score, feedback = password_strength_checker(pwd)
        print(f"Your Score:  {score}/5")
        for tips in feedback:
            print(tips)

        if score <5:
            print("----------------------------")
            print(" Still Weak! Try Again !!")
            print("----------------------------")

        
        else:
            print("--------------------------------------------")
            print(" Your password is strong enough. Very good")
            print("--------------------------------------------")
            break