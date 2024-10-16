#Task 1
"""class Animal(object):
    def __init__(self, s, n):
       self._state = s
       self._size = n

    def feed(self):
        self._size += 1
        print(self._state, " fed")

    def getState(self):
       return self._state

    def getSize(self):
       return self._size

class Fish(Animal):
    def __init__(self, s, n):
        super().__init__(s,n)
        self.__maxsize = 0

    def setMaxSize(self, m):
        self.__maxSize = m
      
    def feed(self):
        self._size += 2
        print(self._state, " fed")
        if self._size >= self.__maxSize:
            self._state = "BIG FISH"

class Duck(Animal):
    def __init__(self, s, n):
        super().__init__(s,n)

    def feed(self):
        Animal.feed(self)
        if self._size == 5:
            self._state = "BIG DUCK" 

#Main
thisFish = Fish("little fish",0)
thisFish.setMaxSize(3)
thisDuck = Duck("little duck",0)
for count in range(1,3):
    thisDuck.feed()
    print(thisDuck.getState())
    thisFish.feed()
    print(thisFish.getState())
"""

#Task 2
"""class Order(object):
    def __init__(self):
        self.__ProductsOrdered = []
        self.__Status = OrderStatus()

    def append(self, product):
        self.__ProductsOrdered.append(product)

    def Status(self):
        return self.__Status.hasShipped()

    def getProductsOrdered(self, productNum):
        Product = self.__ProductsOrdered[productNum]
        return Product

    def ProductID(self, product):
        return product.ProductID()

    def ProductPrice(self, product):
        return product.ProductPrice()

class OrderStatus(object):
    def __init__(self):
        self.__hasShipped = False

    def hasShipped(self):
        return self.__hasShipped

    def setHasShipped(self):
        if self.__hasShipped == False:
            self.__hasShipped = True


class Product(object):
    def __init__(self, productID, productPrice):
        self.__productID = productID
        self.__productPrice = productPrice

    def ProductID(self):
        return self.__productID

    def ProductPrice(self):
        return self.__productPrice


product1 = Product("beans", 0.45)
product2 = Product("eggs", 1.25)

myOrder = Order()
myOrder.append(product1)
myOrder.append(product2)

print(myOrder.Status())

Product0 = myOrder.getProductsOrdered(0)
Product1 = myOrder.getProductsOrdered(1)

print(myOrder.ProductID(Product0))
print("£"+str(myOrder.ProductPrice(Product0)))

print(myOrder.ProductID(Product1))
print("£"+str(myOrder.ProductPrice(Product1)))
"""

#Task 3
class Llama(object):
    def __init__(self, name, gender, age):
        self.__name = name
        self.__gender = gender
        self.__age = age
        self.__type = "Basic"

    def calcValue(self):
        self.__value = 0.0
        Type = self.__type
        age5less = self.__age - 5
        age5more = self.__age + 5
        ageUnder5 = 5 - self.__age 
        if self.__age == 5:
            if self.__gender == "Male":
                self.__value = 1000
            else:
                self.__value = 1200
        elif age5less < 0:
            if self.__gender == "Male":
                val = 1000 - 50*ageUnder5
                self.__value = val
            else:
                val = 1200 - 50*ageUnder5
                self.__value = val
        elif age5more > 0:
            if self.__gender == "Male":
                val = 1000 - 100*age5less
                self.__value = val
            else:
                val = 1200 - 100*age5less
                self.__value = val
        else:
            self.__value = 1000.00

        if Type == "Nibbler":
            self.__value *= 0.9
        elif Type == "Spitter":
            self.__value *= 0.75

    def getName(self):
        return self.__name

    def getGender(self):
        return self.__gender

    def getAge(self):
        return self.__age

    def setType(self):
        Type = input("Enter Llama type (Nibbler/Spitter/Basic): ")
        if Type == "Nibbler" and self.__age > 5:
            Type = "Nog"
        self.__type = Type

    def getType(self):
        return self.__type

    def getValue(self):
        return self.__value

    def isNibbler(self):
        if self.__type == "Nibbler":
            return True
        else:
            return False

    def isSpitter(self):
        if self.__type == "Spitter":
            return True
        else:
            return False

    def isNog(self):
        if self.__type == "Nog":
            return True
        else:
            return False

    def display(self):
        print("The details of the llama named",self.getName(),"are as follows:")
        print("Gender -",self.getGender())
        print("Age -",self.getAge())
        print("Type -",self.getType())
        print("Value - £"+str(self.getValue()))

def menu():
    print("""1. Create and name llama;
2. Show details of llama;
3. Set type of llama;
4. Check type;
5. Exit program.""")

def choice():
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter an integer between 1 & 5")
        choice = int(input("Enter your choice: "))
    return choice

def checkType(thisLlama):
    try:
        typeChoice = int(input("Enter your choice (1-3): "))
    except ValueError:
        print("Please enter an integer between 1 & 3")
        typeChoice = int(input("Enter your choice (1-3): "))
    if typeChoice == 1:
        Nibbler = thisLlama.isNibbler()
        if Nibbler:
            print("This llama is a Nibbler")
    elif typeChoice == 2:
        Spitter = thisLlama.isSpitter()
        if Spitter:
            print("This llama is a Spitter")
    elif typeChoice == 3:
        Nog = thisLlama.isNog()
        if Nog:
            print("This llama is a Nog")
    else:
        print("Choice not applicable")
        checkType(thisLlama)
    
            
def sim(selected_choice,llama,llamaCount):
    noexit = True
    while noexit:    
        if selected_choice == 1:
            name = input("Enter a name for your llama: ")
            gender = input("Enter a gender for your llama: ")
            age = int(input("Enter an age (in years) for your llama: "))
            llama = Llama(name, gender, age)
            llamas.append(llama)
            llamaCount += 1
            menu()
            selected_choice = choice()
            sim(selected_choice,llama,llamaCount)
        elif selected_choice == 2:
            llamaChoice = int(input("Select the number of which llama you want to view details of: "))
            if llamaChoice <= llamaCount:
                thisLlama = llamas[llamaChoice]
                thisLlama.calcValue()
                thisLlama.display()
            else:
                print("Invalid choice for llama number")
            menu()
            selected_choice = choice()
            sim(selected_choice,llama,llamaCount)
        elif selected_choice == 3:
            llamaChoice = int(input("Select the number of which llama you want to set type of: "))
            if llamaChoice <= llamaCount:
                thisLlama = llamas[llamaChoice]
                thisLlama.setType()
            else:
                print("Invalid choice for llama number")
            menu()
            selected_choice = choice()
            sim(selected_choice,llama,llamaCount)
        elif selected_choice == 4:
            llamaChoice = int(input("Select the number of which llama you want to check type of: "))
            if llamaChoice <= llamaCount:
                thisLlama = llamas[llamaChoice]
                print("1. Check if llama is a Nibbler")
                print("2. Check if llama is a Spitter")
                print("3. Check if llama is a Nog")
                checkType(thisLlama)
            else:
                print("Invalid choice for llama number")
            menu()
            selected_choice = choice()
            sim(selected_choice,llama,llamaCount)
        elif selected_choice == 5:
            noexit = False
            break
        else:
            print("Please enter an integer between 1 & 5")
            menu()
            selected_choice = choice()
            sim(selected_choice,llama,llamaCount)
    return llamaCount

#Main
llama = Llama("","",0)
llamaCount = 0
llamas = []
menu()
selected_choice = choice()
sim(selected_choice,llama,llamaCount)
