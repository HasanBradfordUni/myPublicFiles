#Max num from file, method 2

#Now l;et's use the second method

#Opening and reading form the file once again
file = open("nums.txt")
fileContents = file.readlines()

#Now there is an in-built method called "max"

maxNum = max(fileContents)

print("The maximum number in the file is:",maxNum)

"""This method, although it is faster does have drawbacks
for exmample you can't output what line this number is on
in the file"""
