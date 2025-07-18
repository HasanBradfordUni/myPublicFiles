from .transaction_notes import TransactionNotes
from .reporting import Reporting

class Stack:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.array = [""]*self.maxsize
        self.pointer = -1
        self.used_positions = 0

    def push(self,item):
        full = self.isFull()
        if full:
            print("Not available")
        else:
            self.array[self.pointer+1] = item
            self.pointer = self.pointer+1
            self.used_positions = self.used_positions + 1

    def pop(self):
        empty = self.isEmpty()
        if empty:
            print("The stack is empty, cannot dequeue", self.array[self.pointer])
        else:
            chore = self.array[self.pointer]
            self.pointer = self.pointer - 1
            self.used_positions = self.used_positions - 1
            return chore

    def isFull(self):
        if self.used_positions == self.maxsize:
            return True
        else:
            return False

    def isEmpty(self):
        if self.used_positions == 0:
            return True
        else:
            return False

    def peek(self):
        return self.array[self.pointer]

    def show_all(self):
        self.list = []
        for x in range (0, self.pointer+1):
            self.list.append(self.array[x])
        return self.list

class FinanceOptions:
    def __init__(self):
        self.__TotalIncome = 0
        self.__TotalExpenses = 0
        self.__balance = self.__TotalIncome - self.__TotalExpenses
        self.BrokieStatus = None
        self.FinanceHistory = Stack(100)
        self.ReportGenerator = Reporting()
        self.NotesManager = TransactionNotes()
        self.options = {1: "1. Input income", 2: "2. Input expenses", 3: "3. View Balance", 4: "4. View total income",
                        5: "5. View total expenses", 6: "6. View total finance history", 7: "7. Generate Report", 8: "Go Back"}

    def displayMenu(self):
        print("Below are the finance menu options\n")
        for option in self.options.values():
            print(option)

    def getChoice(self):
        print("\nEnter your choice from the options above: ")
        choice = 0
        while choice not in self.options.keys():
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
        return choice

    def IncomeInput(self, income):
        self.__TotalIncome += income
        self.FinanceHistory.push(+income)

    def ExpensesInput(self, expenses):
        self.__TotalExpenses += expenses
        self.FinanceHistory.push(-expenses)

    def IncomeOutput(self):
        return self.__TotalIncome

    def ExpensesOutput(self):
        return self.__TotalExpenses

    def TotalBalanceCalc(self):
        self.__balance = self.__TotalIncome - self.__TotalExpenses
        return self.__balance

    def BrokieMeter(self):
        if self.__balance < 1000000:
            self.BrokieStatus = True
        else:
            self.BrokieStatus = False
        return self.BrokieStatus