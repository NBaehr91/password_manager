import random
import string

# Function to generate a password
def password_generator(minLength, digits=True, specChar=True):
    letter = string.ascii_letters
    digi = string.digits
    spCh = string.punctuation
    
    characters = letter
    if digits:
        characters+=digi
    if specChar:
        characters+=spCh
        
    firChar = random.choice(characters)
    
    passWord = firChar
    
    pwGood = False
    chkNum = False
    chkSpChar = False
    
    while not pwGood or len(passWord) < minLength:
        addChar = random.choice(characters)
        
        if addChar == passWord[len(passWord) - 1]:
            continue
        passWord += addChar
        
        if addChar in digi:
            chkNum = True
        elif addChar in spCh:
            chkSpChar = True
            
        pwGood = True
        if digits:
            pwGood = chkNum
        if specChar:
            pwGood = pwGood and chkSpChar
            
    return passWord


# Test the password generator
"""
makePassword = True
while makePassword:
    set_passLength = int(input("Minimum password length: "))
    set_hasDigits = input("Include numbers (y/n)? ").lower() == "y"
    set_hasSpecChar = input("Include special characters (y/n)? ").lower() == "y"
    
    newPassword = password_generator(set_passLength,set_hasDigits,set_hasSpecChar)
    
    print("\n","New password: ", newPassword,"\n")
    makePassword = input("Make a new password (y/n)? ").lower == "y"
"""