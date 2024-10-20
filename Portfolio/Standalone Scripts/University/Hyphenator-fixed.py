# Hyphenator_fixed.py

""" Inserts hyphens into a non-empty input string as follows:

Example: 
abcdef becomes ab-cd-ef
abcde becomes  ab-c-de

"""
### This program intentionally has at least one error in it!

s = input('Enter a string: ')

n = len(s)

if n%2 != 0:        # s has odd length           
    m = int(n/2)  
   
    first = s[0:m]

    middle = s[m]

    second = s[m+1:]
    
    h = first + '-' + middle + '-' + second                 

else:                    # s has even length
    m = int(n/2)  
   
    first = s[0:m]

    second = s[m:]
    
    h = first + '-' + second

# final output
print(s,'becomes',h)
