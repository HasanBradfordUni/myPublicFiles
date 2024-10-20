def isSquare(width, length):
    if width == length:
        return True
    else:
        return False

def calcSumDigits(string):
    thisSum = 0
    average = 0
    for i in string:
        thisSum += int(i)
    average = thisSum / len(string)
    return thisSum, average

def stringBalanced(s1, s2):
    balanced = True
    for char in s1:
        if char not in s2:
            balanced = False
    return balanced

def countChars(string):
    letters = 0
    digits = 0
    special = 0
    for char in string:
        charValue = ord(char)
        if 32 < charValue < 48 or 57 < charValue < 65:
            special += 1
        elif 47 < charValue < 58:
            digit += 1
    return letters, digits, special

if __name__ == "__main__":
    string1 = input("Enter a string: ")
    string2 = input("Enter another string: ")
    if stringBalanced(string1,string2):
        print("The strings contain the same characters (they are balanced)")
    else:
        print("The strings don't contain the same characters (they aren't balanced)")
