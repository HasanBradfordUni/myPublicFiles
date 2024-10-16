from math import log

def bubbleTest(n):
    return n**2

def mergeTest(n):
    return n * round(log(n), 2)

def bubbleSort(sortList):
    sorted = False
    length = len(sortList)
    swaps = 0
    while not sorted:
        sorted = True
        for i in range(length - 1):
            if sortList[i] > sortList[i+1]:
                swaps += 1
                temp = sortList[i]
                sortList[i] = sortList[i+1]
                sortList[i+1] = temp
                sorted = False
    return sortList, swaps

def bubbleSort1(sortList):
    sorted = False
    length = len(sortList)
    swaps = 0
    while not sorted:
        sorted = True
        for i in range(length - 1):
            if sortList[i] > sortList[i+1]:
                swaps += 1
                temp = sortList[i]
                sortList[i] = sortList[i+1]
                sortList[i+1] = temp
                sorted = False
        length -= 1
    return sortList, swaps

def mergeSort(sortList):
  swaps = 0
  if len(sortList) > 1:
  
    m = len(sortList)/2
    m = round(m, 0)
    m = int(m)
    array1 = sortList[0:m]
    array2 = sortList[m:]

    mergeSort(array1)
    mergeSort(array2)

    i = j = k = 0
    
    while i < len(array1) and j < len(array2):
      if array1[i] <= array2[j]:
          swaps += 1
          sortList[k] = array1[i]
          i += 1
      else:
          swaps += 1
          sortList[k] = array2[j]
          j += 1
      k += 1
      
    while i < len(array1):
      sortList[k] = array1[i]
      i += 1
      k += 1

    while j < len(array2):
      sortList[k] = array2[j]
      j += 1
      k += 1

  return sortList, swaps

def getList():
    numList = []
    entry = input("Add an integer number to the list or use a list: ")
    while entry != '':
        if entry[0] == "[":
            thisEntry = entry.strip("[]").split(",")
            theList = list(thisEntry)
            for item in theList:
                numList.append(int(item))
            entry = input("Add an integer number to the list or use a list: ")
        else:
            try:
                numList.append(int(entry))
            except:
                print("That is not a valid data type!")
            entry = input("Add an integer number to the list: ")
    return numList

"""numList = getList() 
print("Sorting algorithms given:")
print(numList)
print("Bubble sort returns")
print(bubbleSort(numList))
print(bubbleSort1(numList))
print("Merge sort returns")
print(mergeSort(numList))"""
for num in range(3):
    n = int(input("What size list do you want to test? "))
    print("Bubble sort takes:")
    print(bubbleTest(n))
    print("Merge sort takes:")
    print(mergeTest(n))
input()
