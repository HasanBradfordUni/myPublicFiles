# FormatPlay.py
""" A short script that illustrates formatted print."""

from math import pi
x = 355
y = 113
z = float(x)/float(y)
err = abs(z - pi)
print('\nNumerator   Denominator   Quotient      Error')
print('-----------------------------------------------')
print('%9d %9d    %22.15f %10.6e' % (x,y,z,err)) 
