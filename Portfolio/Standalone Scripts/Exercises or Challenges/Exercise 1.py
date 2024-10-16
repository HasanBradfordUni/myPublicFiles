from math import log

def LinearTest(n, tests):
        return (n+12)

def BinaryTest(n, tests):
        return round(log(n), 3)

def getVal():
        try:
                x = int(input("Enter an integer to search for: "))
                return x
        except ValueError:
                print("Value not an integer")
                getVal()
        

def linearSearch(searchList, searchVal):
        count = 0
        for i in range(0, len(searchList)):
                count += 1
                if searchList[i] == searchVal:
                        return i, count
        return "Value not found", count

def binarySearch(searchList, searchVal):
    start = 0
    end = len(searchList) - 1
    count = 0
    while start <= end:
        count += 1
        mid = (start + end) // 2
        if searchList[mid] == searchVal:
            return mid, count
        elif searchList[mid] < searchVal:
            start = mid + 1
        elif searchList[mid] > searchVal:
            end = mid - 1
    return "Value not found", count

"""def recursiveBinarySearch(searchList, searchVal, start, end):
        found = False

        while start <= end and found == False:
                midpoint = (start + end) // 2
                if searchList[midpoint] == searchVal:  
                    found = True
                    return midpoint
                elif searchList[midpoint] < searchVal:
                    start = midpoint + 1  
                    recursiveBinarySearch(searchList, searchVal, start, end)
                else: 
                    end = midpoint - 1  
                    recursiveBinarySearch(searchList, searchVal, start, end)

        if not found:
                return "Value not found"
"""

def generateList():
        newList = []
        start = 1
        endNum = int(input("Enter a max number for the list: "))
        while start <= endNum:
                newList.append(start)
                start += 1
        return newList
                
"""searchList = generateList()
print(searchList)
x = getVal()
print(linearSearch(searchList, x))
print(binarySearch(searchList, x))"""
for num in range(5):
        n = int(input("What is the length of list you want to test for? "))
        tests = int(input("How many tests do you want to do? "))
        print("Linear search (for 1000 tests) takes:")
        print(LinearTest(n, tests))
        print("Binary search (for 1000 tests) takes:")
        print(BinaryTest(n, tests))
#print(recursiveBinarySearch(searchList, x, 0, 9))
input()
