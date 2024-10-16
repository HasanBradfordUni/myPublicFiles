#Today we will be looking at String methods and conditional statements

"""This program will closely examine some of the various string methods and also
will look at conditional statements (if, elif, else) and also the boolean operators"""

#below is an example of a string
myString = "Hello, This is a string!"

#First we'll start with string slicing
#print(myString[:5]) #This will print out the first 5 characters of 'myString'
#print(myString[10:]) #This will print from character 10 till the end
#print(myString[6:11]) #This will print from character 6 until character 10 (not including 11)

#You can also get a single character from a string, this time we'll ask the user
#character = int(input("Enter a character number (index) to retrieve from string: "))
#print("The character is:",myString[character])

#Okay, so now we will use one of the many string methods

#print(myString.count('s'))
#This will print out the amount of times a certain character appears in our string

#Now we can use a different method
#newString = myString.replace('Hello', 'Bye')
#print(newString)
#So this will replace any substring with another substring, you have to store it as a new string

#There is also a 'lower' method and 'upper' method
#print(myString.lower())
#print(myString.upper())

#Now moving onto if statements (conditional statements)
"""if myString.islower() | myString.isupper():
    print("String is uniform")
else:
    print("String is irregular")"""

#Let's do an example with numbers
"""num1 = int(input("Enter a number: "))
num2 = int(input("Enter another number: "))

if (num1 > 5) & (num2 <= 5):
    print("Success")
elif (num1 == 5) | (num2 > 5):
    print("Neither a fail nor a success")
else:
    print("Fail")"""

otherString = input("Enter a string to compare to myString: ")

if (myString.islower() | myString.isupper()) & (otherString.islower() | otherString.isupper()):
    print("Both strings are regular")
elif not (myString.islower() | myString.isupper()) and not (otherString.islower() | otherString.isupper()):
    print("Both strings are irregular")
else:
    print("The strings aren't similar in terms of case")

if myString[:5].lower() in otherString.lower():
    print("Both are greetings!")
else:
    print("One of the strings is not a greeting")

if myString == otherString:
    print("The strings match!")
else:
    print("The strings don't match")









    


