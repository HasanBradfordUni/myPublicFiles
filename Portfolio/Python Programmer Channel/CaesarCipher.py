#Caesar Cipher

#Now we have to define the function
def encrypt(text, key):
    result = '' #setting up an empty variable first
    #Now it's a for loop
    for char in text:
        if (char.isupper()):
            result += chr((ord(char)+key-65)%26+65)
            #Above, that is the formula for the encryption
        else:
            result += chr((ord(char)+key-97)%26+97)
    #Now all we have to do is return the final result
    return result

#First we will ask the user for some input
text = input("Enter some text to encrypt: ")

#NBow we will ak the user for the cipher key
#You can also use exception handling for the key
while True:
    try:
        key = int(input("Enter the key (1-25): "))
        break
    except:
        print("Key must be an integer!")

#Finally, let's call the function
encrypted = encrypt(text, key)
print("The encrypted message is:",encrypted)
