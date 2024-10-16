#Max num from file, method 1

#First, let's open and read from the file
file = open("nums.txt")
fileContents = file.readlines()

#The first methiod is using a for loop
#Nearly forgot the variable
maxNum = 0
thisLine = 0
for count, line in enumerate(fileContents):
    num = int(line.strip())
    if num > maxNum:
        maxNum = num
    #using this method, we can aslo output the line num
        thisLine = count

print("The maximum number is:",maxNum)
print("It is on line:",thisLine)
