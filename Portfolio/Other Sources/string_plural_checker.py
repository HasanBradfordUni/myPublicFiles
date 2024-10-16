#take a string input and store it
s = input("Enter a string: ")

#use an if statement to check if the last 2 characters are equal to "es"
if s[len(s)-2:] == "es" : #len(s) - 2 gets the index value of the second last character and colon (:) means it goeds to end of string
    print('Plural') #prints 'plural'
else: #if the above statement is false, goes to this
    print('Not  Plural') #prints 'not plural'
