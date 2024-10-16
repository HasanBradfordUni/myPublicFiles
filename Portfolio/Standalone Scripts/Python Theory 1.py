#Conversion program
print("Conversion options: ")
print("""1. Binary to Denary
2. Denary to Binary
3. Hexadecimal to Denary
4. Denary to Hexadecimal
5. Hexadecimal to Binary
6. Binary to Hexadecimal""")
conversion = int(input("\nEnter selected conversion (1-6): "))
if conversion == 1:
    print("Binary to Denary selected")
    binaryNum = str(input("Enter an 8-bit binary number: "))
    firstDigit = int(binaryNum[0]) * 128
    secondDigit = int(binaryNum[1]) * 64
    thirdDigit = int(binaryNum[2]) * 32
    fourthDigit = int(binaryNum[3]) * 16
    fifthDigit = int(binaryNum[4]) * 8
    sixthDigit = int(binaryNum[5]) * 4
    seventhDigit = int(binaryNum[6]) * 2
    eigthDigit = int(binaryNum[7]) * 1
    denaryNum = firstDigit + secondDigit + thirdDigit + fourthDigit + fifthDigit + sixthDigit + seventhDigit + eigthDigit
    print("The binary value",binaryNum,"in denary is",denaryNum)
elif conversion == 2:
    print("Denary to Binary selected")
    denaryNum = int(input("Enter a denary number (0-255): "))
    firstDigit = denaryNum // 128
    secondDigit = (denaryNum - 128) // 64
    thirdDigit = (denaryNum - 192) // 32
    fourthDigit = (denaryNum - 224) // 16
    fifthDigit = (denaryNum - 240) // 8
    sixthDigit = (denaryNum - 248) // 4
    seventhDigit = (denaryNum - 252) // 2
    eigthDigit = (denaryNum - 254) // 1
    print("The denary value",denaryNum,"in binary is",str(firstDigit)+str(secondDigit)+str(thirdDigit)+str(fourthDigit)+str(fifthDigit)+str(sixthDigit)+str(seventhDigit)+str(eigthDigit))
elif conversion == 3:
    print("Hexadecimal to Denary selected")
    hexNum = str(input("Enter a 2 digit hexadecimal number: "))
    if hexNum[0] == "A":
        firstDigit = 10 * 16
    elif hexNum[0] == "B":
        firstDigit = 11 * 16
    elif hexNum[0] == "C":
        firstDigit = 12 * 16
    elif hexNum[0] == "D":
        firstDigit = 13 * 16
    elif hexNum[0] == "E":
        firstDigit = 14 * 16
    elif hexNum[0] == "F":
        firstDigit = 15 * 16
    else:
        firstDigit = int(hexNum[0]) * 16
    if hexNum[1] == "A":
        secondDigit = 10 * 1
    elif hexNum[1] == "B":
        secondDigit = 11 * 1
    elif hexNum[1] == "C":
        secondDigit = 12 * 1
    elif hexNum[1] == "D":
        secondDigit = 13 * 1
    elif hexNum[1] == "E":
        secondDigit = 14 * 1
    elif hexNum[1] == "F":
        secondDigit = 15 * 1
    else:
        secondDigit = int(hexNum[1]) * 1
    denaryNum = firstDigit + secondDigit
    print("The hexadecimal value",hexNum,"in denary is",denaryNum)
elif conversion == 4:
    print("Denary to Hexadecimal selected")
    denaryNum = int(input("Enter a denary number (0-255): "))
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
    else:
        firstDigit = firstDigit
    if secondDigit == 10:
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
    else:
        secondDigit = secondDigit
    print("The denary value",denaryNum,"in hexadecimal is",str(firstDigit)+str(secondDigit))



                      
