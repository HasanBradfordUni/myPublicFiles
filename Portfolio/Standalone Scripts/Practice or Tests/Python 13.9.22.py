#starter
"""def feed(state, size):
    size += 1
    print("Fish fed!")
    if size == 5:
        state = "FISH"
    return state, size

thisFishState = "Fish"
thisFishSize = 1
print(thisFishState,"is of size",thisFishSize)
while thisFishState != "FISH":
    thisFishState, thisFishSize = feed(thisFishState, thisFishSize)
print("It is now a big",thisFishState)
"""
#Task 1
"""class Animal(object):
    def __init__(self, s, n):
       self.__state = s
       self.__size = n

    def feed(self):
       self.__size += 1
       if self.__size == 5:
          self.__state = "FISH"

    def getState(self):
       return self.__state

    def getSize(self):
       return self.__size
"""
#Task 2
"""thisFish = Animal("Fish", 1)
 
print(thisFish.getState())
print("is of size",thisFish.getSize())

while thisFish.getState() != "FISH":
   thisFish.feed()

print("It is now a big") 
print(thisFish.getState())
"""

#Task 3
class Car(object):
    def __init__(self, reg, make):
        self.__mileage = 0
        self.__make = make
        self.__reg = reg
        self.__dateOfInspection = None

    def get_mileage(self):
        return self.__mileage

    def get_make(self):
        return self.__make

    def get_reg(self):
        return self.__reg

    def get_date(self):
        return self.__dateOfInspection

    def inspection(self):
        self.__mileage = int(input("What is current mileage on inspection? "))
        self.__dateOfInspection = input("What is date of inspection? ")

#Testing data
print("Welcome to the official car garage!")
Merc1 = Car("LL16 HYJ","Mercedes E-Class")
print("Merc1 status\nReg:",Merc1.get_reg(),"\nMake:",Merc1.get_make(),"\nMileage:",Merc1.get_mileage(),"\nInspection date:",Merc1.get_date())
print("Inspection has taken place!")
Merc1.inspection()
print("Merc1 status\nReg:",Merc1.get_reg(),"\nMake:",Merc1.get_make(),"\nMileage:",Merc1.get_mileage(),"\nInspection date:",Merc1.get_date())
Audi1 = Car("A4 NNB","Audi A4")
print("Audi1 status\nReg:",Audi1.get_reg(),"\nMake:",Audi1.get_make(),"\nMileage:",Audi1.get_mileage(),"\nInspection date:",Audi1.get_date())
print("Inspection has taken place!")
Audi1.inspection()
print("Audi1 status\nReg:",Audi1.get_reg(),"\nMake:",Audi1.get_make(),"\nMileage:",Audi1.get_mileage(),"\nInspection date:",Audi1.get_date())
Merc2 = Car("HJ18 FGD","Mercedes A-Class")
print("Merc2 status\nReg:",Merc2.get_reg(),"\nMake:",Merc2.get_make(),"\nMileage:",Merc2.get_mileage(),"\nInspection date:",Merc2.get_date())
print("Inspection has taken place!")
Merc2.inspection()
print("Merc2 status\nReg:",Merc2.get_reg(),"\nMake:",Merc2.get_make(),"\nMileage:",Merc2.get_mileage(),"\nInspection date:",Merc2.get_date())
print("That is all for today!")
input("Press 'enter' to exit")
exit()
