# ShowSimpleMath.py

""" Module contains a script that uses the built-in
module math and the user-written module SimpleMath.

It compares the accuracy of the SimpleMath functions sqrt,
cos, and sin with their counterparts in the math module"""
    
import math
import SimpleMath

# Check out the square root function
x = int(input(' Compute the square root of x = '))
MySqrt = SimpleMath.sqrt(x)
TrueSqrt = math.sqrt(x)
print('SimpleMath.sqrt(x) = %12.8f\n      math.sqrt(x) = %12.8f \n' % (MySqrt,TrueSqrt))






    