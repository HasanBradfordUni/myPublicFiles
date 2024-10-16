#Numpy tips and tricks 2
import numpy as np

#We have to define data types for an array
dt = np.dtype([('name', np.str_, 16),
               ('age', np.int32),
               ('weight', np.float64)])

#Now we can create a structured array
data = np.array([('Jake', 19, 74.5),
                 ('Sally', 23, 64.3),
                 ('Jack', 16, 78.9)], dtype=dt)

#print(data)

#Now let's run it

#There are also more useful fetaures to this

print("Names:",data['name'])
print("Ages:",data['age'])
print("Weights:",data['weight'])

#You can also change a field directly
data['weight'][0] = 75.7

print("New weights:",data['weight'])

#You can also print out a record like this
print(data[0]['name'],"has info:",data[0])
