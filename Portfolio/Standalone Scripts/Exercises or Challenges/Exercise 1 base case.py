x = 4

def linearSearch(searchList, searchVal):
	for i in searchList:
		if i == searchVal:
			return i
	return Value not found

def binarySearch(searchList, searchVal):
	start = 0
	end = len(searchList) - 1
	while start <= end:
		mid = (start + end) // 2
		if searchList[mid] == searchVal:
			return mid
		elif searchList[mid] < searchVal:
			start = mid
		elif searchList[mid] > searchVal:
			end = mid
	return Value not found

searchList = [1,2,3,4,5,6,7,8,9,10]
print(linearSearch(searchList, x))
print(binarySearch(searchList, x))
input()
