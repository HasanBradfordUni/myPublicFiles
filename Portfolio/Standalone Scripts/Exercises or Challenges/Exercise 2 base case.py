def bubbleSort(sortList):
	sorted = False
	length = len(sortList)
	while !sorted:
		for i in range(length - 1):
			if sortList[i] > sortList[i+1]:
				sortList[i] = sortList[i+1]
				sortList[i+1] = sortList[i]
				sorted = False
	return sortList

def mergeSort(sortList):
	mid = len(sortList) // 2
	leftHalf = sortList[:mid]
	rightHalf = sortList[mid:]
	if len(sortList) > 1:
		mergeSort(leftHalf)
		mergeSort(rightHalf)

numList = []
for i in range(6):
	print("Add an integer number to the list: ")
	numList.append(int(input()))
print("Bubble sort given:")
print(numList)
print("Bubble sort returns")
print(bubbleSort(numList))
input()
