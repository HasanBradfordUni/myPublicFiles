#Numpy tips and tricks 4
import numpy as np
import timeit

#First we will create two random number arrays
a = np.random.rand(100000)
b = np.random.rand(100000)

def dot_product1():
    dot_product = 0
    for num in range(len(a)):
        dot_product += a[num] * b[num]
    print(dot_product)

def dot_product2():
    dot_product = np.dot(a, b)
    print(dot_product)

time1 = timeit.timeit(lambda: dot_product1, number=1)

time2 = timeit.timeit(lambda: dot_product2, number=1)

"""Here we have put the two dot_product codes in their
own functions and we're going to time how long they each
take to run only 1 time"""

print("Function 1 took",time1,"seconds to run")
print("Function 2 took",time2,"seconds to run")

#We can also use vectorisation with angles

angles_deg = np.array([0,30,45,60,90])

#Now we will use the vectorisation to convert the angles
angles_rad = np.radians(angles_deg)

print(angles_rad)
