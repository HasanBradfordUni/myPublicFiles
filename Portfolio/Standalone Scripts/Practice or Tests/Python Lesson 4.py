#Task 3
"""partNum = input("Enter part number: ")
oldModels = 0
totalParts = 0
if len(partNum) != 4:
    print("Invalid Part Num")
    partNum = input("Enter part number: ")
while partNum != "9999":
    totalParts += 1
    parts = partNum[3]
    if parts == "6" or parts == "7" or parts == "8":
        oldModels += 1
    partNum = input("Enter part number: ")
print("There are",totalParts,"total parts")
print("There are",oldModels,"old models")
"""

#Task 4
total1 = 0
total2 = 0
total3 = 0
for num in range(30):
    test1 = int(input("Enter score for pupil "+str(num+1)+" and test 1: "))
    test2 = int(input("Enter score for pupil "+str(num+1)+" and test 2: "))
    test3 = int(input("Enter score for pupil "+str(num+1)+" and test 3: "))
    average = (test1+test2+test3) // 3
    print("Average for pupil "+str(num+1)+" is",average)
    total1 += test1
    total2 += test2
    total3 += test3
totalAverage = (total1+total2+total3) // 90
print("Average for full class is:",totalAverage)
