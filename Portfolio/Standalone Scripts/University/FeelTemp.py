# FeelTemp.py

""" FeelTemp is a function of temperature and wind.

Solicits temperature and wind via
input and then displays the associated windchill
temperature."""

# Input values
# Temp = int(input('Enter a temperature <= 50F :  '))
# Wind = int(input('Enter a wind speed  >= 3mph:  '))

Temp = 32
Wind = 20

# Model parameters
A = 35.74; B = .6215; C = -35.75; D = .4275; e = .16

# Compute and display the associated feeling temperature...
FT= (A+B*Temp) + (C+D*Temp)*Wind**e

print(FT)
#print('                   FeelTemp:  %14.12f' % FT)
#print('                   FeelTemp:  %2d' % FT)






