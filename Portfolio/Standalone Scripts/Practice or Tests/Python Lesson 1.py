"""oldMileage = int(input("What was the car mileage the last time the car was filled up? "))
newMileage = int(input("What is the car mileage now? "))
tankLitres = float(input("How many litres were taken to fill the tank? "))
miles = newMileage - oldMileage
gallons = tankLitres * 4.546
milesPerGallon = miles / gallons
print("Miles per gallon =",round(milesPerGallon, 3),"MPG")

kilos = float(input("Input a mass in kilos: "))
pounds = float(input("Input a mass in pounds: "))
kilosInPounds = kilos * 2.205
poundsInKilos = pounds / 2.205
print(kilos,"kilos in pounds is:",kilosInPounds)
print(pounds,"pounds in kilos is:",poundsInKilos)
"""
"""number = int(input("Enter a 3 digit number: "))
hundreds = number // 100
units = number % 10
tens = number % 100
tens -= units
tens = tens / 10
print(number,"has",hundreds,"hundreds",tens,"tens and",units,"units")
"""
students = int(input("How many students are there? "))
books = int(input("How many books are there? "))
booksPerStudent = books // students
booksLeftOver = books % students
print("There are",booksPerStudent,"books per student and",booksLeftOver,"books left over")
