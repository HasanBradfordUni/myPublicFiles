#Circular array
class CarsQueue(object):
    def __init__(self):
        self.array = [" "] * 5
        self.maxsize = 5
        self.front = 0
        self.rear = -1
        self.used_positions = 0

    def isEmpty(self):
        if self.used_positions == 0:
            return True
        else:
            return False

    def isFull(self):
        if self.used_positions == self.maxsize:
            return True
        else:
            return False

    def enQueue(self,item):
        full = self.isFull()
        if full:
            print("Queue is full!")
        else:
            self.rear += 1
            if self.rear == self.maxsize:
                self.rear = 0
            self.array[self.rear] = item
            self.used_positions += 1

    def deQueue(self):
        empty = self.isEmpty()
        if empty:
            print("Queue is empty!")
        elif self.front == self.rear:
            self.front = 0
            self.rear = -1
            self.used_positions = 0
        else:
            item = self.array[self.front]
            self.array[self.front] = " "
            self.front += 1
            self.used_positions -= 1
            print(item)
            return item

    def return_queue(self):
        print(self.array)
        print("Info: Front("+str(self.front)+"),Rear("+str(self.rear)+"),Used Positions("+str(self.used_positions)+")")

#main
cars = CarsQueue()
cars.return_queue()
cars.deQueue()
cars.enQueue(item = "Mercedes Benz - White")
cars.return_queue()
cars.enQueue(item = "Audi A5 - Blue")
cars.return_queue()
cars.enQueue(item = "BMW A-series - Silver")
cars.return_queue()
cars.deQueue()
cars.return_queue()
cars.enQueue(item = "Audi A3 - Red")
cars.return_queue()
cars.enQueue(item = "Mercedes E-Class - Silver")
cars.return_queue()
cars.enQueue(item = "Toyota Auris - Blue")
cars.return_queue()
cars.enQueue(item = "BMW A-series - Silver")
cars.deQueue()
cars.return_queue()
cars.deQueue()
cars.deQueue()
cars.return_queue()


