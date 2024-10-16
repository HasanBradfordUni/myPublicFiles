#Challenge 36
"""numbers1 = [ ]
odd = [ ]
numbers = [ ]
for x in range (10):
    number = int(input("Enter a number to add to array: "))
    if number % 2 == 0:
        numbers1.append(number)
    else:
        odd.append(number)
odd.sort(key=None, reverse=False)
numbers1.sort(key=None, reverse=False)
numbers = odd+numbers1
print(numbers)
"""

#Challenge 7
"""creditCard = input("Enter a credit card number to be verified: ")
checkNum = 0
totalChecks = 0
listNum = [int(i) for i in str(creditCard)]
print(listNum)
#Drop the last digit from the number. The last digit is what we want to check against
creditCard = creditCard[:-1]
print(creditCard)
#Reverse the numbers
CCnumber = int(creditCard)
test_num = 0
while(CCnumber>0):
  #Logic
  remainder = CCnumber % 10
  test_num = (test_num * 10) + remainder
  CCnumber = CCnumber//10
print("The reverse number is : {}".format(test_num))
#Multiply the digits in odd positions (1, 3, 5, etc.) by 2 and subtract 9 to all any result higher than 9
CCnumber = [int(i) for i in str(test_num)]
for num in range (0,len(CCnumber)):
    if num % 2 == 1:
        checkNum = CCnumber[num] * 2
        if checkNum > 9:
            checkNum -= 9
            totalChecks += checkNum
        else:
            totalChecks += checkNum
print(totalChecks)
#The check digit (the last number of the card) is the amount that you would need to add to get a multiple of 10 (Modulo 10)
checkNum = totalChecks % 10
if listNum[9] == checkNum:
    print("Credit Card is VALID")
else:
    print("Credit Card is INVALID")
"""

#Challenge 35
"""import random
User_Num = int(input("Enter a number (0-30): "))
money = int(input("Enter money put in: £"))
CPU_Num = random.randint(0,30)
prime = [2,3,5,7,11,13,17,19,23,29]
even = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
below5 = [0,1,2,3,4]
multiple10 = [10,20,30]
bonus = 0
if CPU_Num in even and prime and below5:
    bonus = 20
elif CPU_Num in below5 and prime:
    bonus = 10
elif CPU_Num in multiple10 and even:
    bonus = 6
elif CPU_Num in even and below5:
    bonus = 4
elif CPU_Num in prime:
    bonus = 5
elif CPU_Num in even:
    bonus = 2
elif CPU_Num in below5:
    bonus = 2
elif CPU_Num in multiple10:
    bonus = 3
else:
    bonus = 1
if User_Num == CPU_Num:
    bet = money*bonus
    print("You win £"+str(bet))
else:
    print("You lose")
    print("The number was",CPU_Num)
"""

#Challenge 30
"""import random
totalDigits = 0
CPUyear = random.randint(2000,2100)
CPUyear = str(CPUyear)
for digit in CPUyear:
    totalDigits += int(digit)
print(totalDigits)
year = int(input("Enter a year to guess: "))
if year == CPUyear:
    print("Correct! The year was",CPUyear)
else:
    print("Wrong! The year was",CPUyear)
"""

#Challenge 40
"""denaryNum = int(input("Enter a denary number: "))
firstDigit = denaryNum // 16
secondDigit = denaryNum % 16
if firstDigit == 10:
    firstDigit = "A"
elif firstDigit == 11:
    firstDigit = "B"
elif firstDigit == 12:
    firstDigit = "C"
elif firstDigit == 13:
    firstDigit = "D"
elif firstDigit == 14:
    firstDigit = "E"
elif firstDigit == 15:
    firstDigit = "F"
elif secondDigit == 10:
    secondDigit = "A"
elif secondDigit == 11:
    secondDigit = "B"
elif secondDigit == 12:
    secondDigit = "C"
elif secondDigit == 13:
    secondDigit = "D"
elif secondDigit == 14:
    secondDigit = "E"
elif secondDigit == 15:
    secondDigit = "F"
print(denaryNum, "in hexadecimal is",str(firstDigit)+str(secondDigit))
"""

#Challenge 19
"""gate = input("Enter logic gate: ")
firstInput = input("Enter first input: ")
secondInput = input("Enter second input: ")
if gate == "OR":
    if firstInput == 1 or secondInput == 1:
        print("Result = 1")
    else:
        print("Result = 0")
elif gate == "AND":
    if firstInput == 1 and secondInput == 1:
        print("Result = 1")
    else:
        print("Result = 0")
elif gate == "XOR":
    if firstInput == 1 and secondInput == 1:
        print("Result = 0")
    elif firstInput == 1 or secondInput == 1:
        print("Result = 1")      
    else:
        print("Result = 0")
"""
#Challenge 34
"""import datetime
day = int(input("Enter the day: "))
month = int(input("Enter the month: "))
year = int(input("Enter the year: "))
date = datetime.datetime(year,month,day)
print(date.strftime("%A"))
"""

#Challenge 23
"""print("Welcome to the official Fibonacci sequence generator")
startNum = int(input("Enter starting number: "))
prevNum = 0
num = startNum
print(startNum)
for x in range(10):
    newNum = num + prevNum
    print(newNum)
    prevNum = num
    num = newNum
"""

#Challenge 13
"""def encrypt(text,key):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if (char.isupper()):
            result += chr((ord(char) + key-65) % 26 + 65)
        else:
            result += chr((ord(char) + key - 97) % 26 + 97)
    return result
text = input("Enter some text to encrypt: ")
key = int(input("Enter the key (1 - 25): "))
print(encrypt(text,key))
"""

#Challenge 20
"""print("Welcome to the official palindrome checker")
word = input("Enter a word to check for palindromes: ")
wordReversed = word[::-1]
if word == wordReversed:
    print(word,"is a palindrome")
else:
    print(word,"is not a palindrome")
"""

#Challenge 37
"""endNum = int(input("Enter a number to end on: "))
for num in range(1,endNum+1):
     mult3 = num % 3
     mult5 = num % 5
     multBoth = num % 15
     if multBoth == 0:
         print("FizzBuzz")
     elif mult3 == 0:
         print("Fizz")
     elif mult5 == 0:
         print("Buzz")
     else:
         print(num)
"""

