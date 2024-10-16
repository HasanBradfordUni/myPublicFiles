#Numpy tips and ticks 3
import numpy as np

a = np.array([1,4,8,6,9,2])

#You can select elements by index

print(a[[1, 5, 2]])

#You can also modify elements like this
a[[1,2,3]] = 0
print(a)
