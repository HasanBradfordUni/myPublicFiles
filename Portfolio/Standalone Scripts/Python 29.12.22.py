#Question 4

def isHarshad(num):
    strNum = str(num)
    digitsAdded = 0
    for digit in strNum:
        digitsAdded += int(digit)
    if num % digitsAdded == 0:
        return True
    else:
        return False

def calcHarshads(num):
    harshads = []
    harshadNum = 0
    thisNum = 1
    while harshadNum < num:
        if isHarshad(thisNum):
            harshads.append(thisNum)
        thisNum += 1
        harshadNum = len(harshads)
    return harshads

num = int(input("Enter a positive integer: "))
harshads = calcHarshads(num)
last = len(harshads) - 1
thatNum = harshads[last]
print("The "+str(num)+"th harshad number is:",thatNum)

#Question 6
"""
def firstInSecond(word1, word2):
    firstInSecond = True
    for char in word1:
        if char not in word2:
            firstInSecond = False
    return firstInSecond

word1 = input("Enter a word: ")
word2 = input("Enter another word: ")
word1 = word1.upper()
word2 = word2.upper()
firstInSecond = firstInSecond(word1, word2)
if firstInSecond:
    print(word1,"can be formed from",word2)
else:
    print(word1,"cannot be formed from",word2)
"""
