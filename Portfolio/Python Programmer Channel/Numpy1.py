#Numpy tips and tricks 1
import numpy as np

a = np.array([5,3,7])
b = 2

print(a+b)
"""Here this is called broadcasting, it allow the operator
addition to be applied between b and a element-wise, even
though b is just a numbver and a is an array it will add
b to each element of a"""

#Now let's run it
