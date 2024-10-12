#Merge sort algorithm
array = [2,4,6,5,3,1,7]

def sort(array):
  if len(array) > 1:
  
    m = len(array)/2
    m = round(m, 0)
    m = int(m)
    array1 = array[0:m]
    array2 = array[m:]

    sort(array1)
    sort(array2)

    i = j = k = 0
    
    while i < len(array1) and j < len(array2):
      if array1[i] <= array2[j]:
          array[k] = array1[i]
          i += 1
      else:
          array[k] = array2[j]
          j += 1
      k += 1
      
    while i < len(array1):
      array[k] = array1[i]
      i += 1
      k += 1

    while j < len(array2):
      array[k] = array2[j]
      j += 1
      k += 1

  return array
print(sort(array))
