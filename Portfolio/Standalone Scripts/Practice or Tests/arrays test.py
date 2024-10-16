#arrays test

class MovesQueue(object):
    def __init__(self):
        self.array = [""] * 5
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
            if self.rear == self.maxsize - 1:
              rear = 0
            else:
              rear += 1
            self.array[self.rear] = item
            self.used_positions += 1

    def deQueue(self):
        item = None
        empty = self.isEmpty()
        if empty:
            print("Queue is empty!")
        else:
            item = self.array[self.front]
            self.used_positions -= 1
            if self.front == self.maxsize - 1:
              front = 0
            else:
              front = front + 1
        return item
            
    def replace(self, item):
      self.array.pop()
      self.array.append(item)
      
    def return_queue(self):
        print(self.array)
        print("Info: Front("+str(self.front)+"),Rear("+str(self.rear)+"),Used Positions("+str(self.used_positions)+")")

# <Main>

turnOrder = [1,2]

while True:
    currentTurn = turnOrder[0]
    print(currentTurn)
    turnOrder.append(currentTurn)
    print(turnOrder)
    turnOrder.remove(turnOrder[0])
    print(turnOrder)
    empty = input()
    if len(empty) != 0:
        break

array = [1,2,3,4,5]

item = array.pop()

print(item)
print(array)

thisQueue = MovesQueue()

while True:
    print("""1. Enqueue
2. Dequeue
3. Replace
4. Print Queue
5. Exit""")
    choice = input()
    if choice == 1:
        item = input("Enter an item to enqueue")
        thisQueue.enQueue(item)
    elif choice == 2:
        thisQueue.deQueue()
    elif choice == 3:
        item = input("Enter an item to replace")
        thisQueue.replace(item)
    elif choice == 4:
        thisQueue.return_queue()
    elif choice == 5:
        break
    else:
        choice = input()

