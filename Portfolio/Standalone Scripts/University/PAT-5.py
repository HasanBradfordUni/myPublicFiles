#Tasks from Pat 5

def largestInList(myList):
    largest = myList[0]
    for i in myList:
        if i > largest:
            largest = i
    return largest

def binarySearch(arr, low, high, x):
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binarySearch(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return binarySearch(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return -1
    

if __name__ == "__main__":
    myList = [1,4,1,5,2,6,9,10,54,69,21]
    print("The list is:",myList)
    num = int(input("Enter a number to search for in the list: "))
    print(f"The number {num} is found at index {binarySearch(myList,0,len(myList),num)} in thr list")
