"""This is a program that will take a string input.
It will put a hyphen in the middle of a given string if it has an even length,
or put a hyphen around the middle character if it has an odd length"""

#take a string input and store it
string = input("Enter a string: ")

#get the length of the string
string_length = len(string)

if string_length % 2 == 0: #checks if the string length is even
    midpoint = int(string_length / 2) #get the midpoint of the string
    #define the new string (with hyphen in middle)
    new_string = string[:midpoint] + "-" + string[midpoint:]
else: #if the above statement is false, goes to this
    midpoint = string_length // 2 #get the midpoint of the string
    #define the new string (with hyphens)
    new_string = string[:midpoint] + "-" + string[midpoint] + "-" + string[midpoint+1:]

print(new_string)    
