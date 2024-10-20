# Hyphenator_broken.py

""" Inserts hyphens into a non-empty input string as follows:

the string is even: for example, abcdef becomes abc-def
the string is odd: for example, abcde becomes  ab-c-de

"""
### This program intentionally has at least one error in it!

s = input('Enter a string: ')

n = len(s)

# s has odd length           
m = int(n/2)  
   
first = s[0:m]

middle = s[m]

second = s[m+1:]
    
h = first + '-' + middle + '-' + second                 

# final output
print(s,'becomes',h)
