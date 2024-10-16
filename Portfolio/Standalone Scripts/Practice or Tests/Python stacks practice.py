#Chores stack simulator
class ChoresStack(object):
    def __init__(self):
        self.maxsize = 5
        self.pointer = -1
        self.used_positions = 0
        self.array = [" "] * 5

    def isEmpty(self):
        if self.pointer == -1:
            return True
        else:
            return False

    def isFull(self):
        end = self.maxsize - 1 
        if self.pointer == end:
            return True
        else:
            return False

    def peek(self):
        data = None
        empty = self.isEmpty()
        if empty:
            print("Stack underflow!")
        else:
            data = self.array[self.pointer]
        return data

    def push(self,data):
        full = self.isFull()
        if full:
            print("Stack overflow!")
        else:
            self.pointer += 1
            self.array[self.pointer] = data
            self.used_positions += 1

    def pop(self):
        data = None
        empty = self.isEmpty()
        if empty:
            print("Stack underflow")
        else:
            data = self.array[self.pointer]
            self.pointer -= 1
            self.used_positions -= 1
        return data
    
    def return_stack(self):
        print(self.array)
        print("Info: Pointer("+str(self.pointer)+") Used Positions("+str(self.used_positions)+")")

#Testing
print("Welcome to the official stack of chores simulator!")
chores = ChoresStack()
chores.return_stack()
chores.push("Clean room")
chores.return_stack()
chores.push("Wash dishes")
chores.peek()
chores.pop()
chores.return_stack()
chores.push("Dust living room")
chores.push("Give car a good wash")
chores.peek()
chores.push("Do the laundry")
chores.push("Feed the bird")
chores.return_stack()
chores.push("Just another chore!")
chores.pop()
chores.peek()
chores.pop()
chores.peek()
chores.pop()
chores.peek()
chores.pop()
chores.pop()
chores.return_stack()
chores.peek()
chores.pop()
print("End of program...")
print("Bye!")



        
