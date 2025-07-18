from transactionNotes import TransactionNotes
from reporting import Reporting

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

  def SeeFinanceHistory(self):
    financeHistory = self.FinanceHistory.show_all()
    #print the finance history one by one, put a comma between if both positive or both negative and new line if different
    for x in range(0, len(financeHistory)-1):
      if financeHistory[x] > 0 and financeHistory[x+1] > 0:
        print(financeHistory[x], ", ", end="")
      elif financeHistory[x] < 0 and financeHistory[x+1] < 0:
        print(financeHistory[x], ", ", end="")
      else:
        print(financeHistory[x])
    return financeHistory

  def TotalBalanceCalc(self):
    self.__balance = self.__TotalIncome - self.__TotalExpenses
    return self.__balance

  def BrokieMeter(self):
    if self.__balance < 1000000:
      self.BrokieStatus = True
    else:
      self.BrokieStatus = False
    return self.BrokieStatus

  def GenerateReport(self):
    print("Generating report...")
    start_date = input("First enter the start date (dd/mm/yyyy): ")
    end_date = input("Also enter the end date for the report (dd/mm/yyyy): ")
    totalIncome, totalExpenses, datedTransactions = self.ReportGenerator.generateReport(start_date, end_date, self.FinanceHistory)
    print("Report generated")
    print("Total income:", totalIncome)
    print("Total expenses:", totalExpenses)
    for transaction in datedTransactions:
      print("Date:",transaction.date)
      print("Amount:",transaction.amount)
      print("Category:",transaction.category)
      if transaction.notes:
        print("Notes:",transaction.notes)
      print()

  def handleChoice(self, choice):
    print()
    match choice:
      case 1:
        income = int(input("Enter income: "))
        date = input("Also enter the date: ")
        self.ReportGenerator.setDate(date)
        self.IncomeInput(income)
        addNote = input("Would you like to add a note? (y/n): ")
        if addNote.lower() == "y":
          self.incomeID = self.ReportGenerator.getID(self.FinanceHistory.used_positions - 1)
          self.NotesManager.addNote(self.incomeID)
        return False
      case 2:
        expenses = int(input("Enter expenses: "))
        date = input("Also enter the date: ")
        self.ReportGenerator.setDate(date)
        self.ExpensesInput(expenses)
        addNote = input("Would you like to add a note? (y/n): ")
        if addNote.lower() == "y":
          self.expenseID = self.ReportGenerator.getID(self.FinanceHistory.used_positions - 1)
          self.NotesManager.addNote(self.expenseID)
        return False
      case 3:
        balance = self.TotalBalanceCalc()
        print("Your current balance is: " + str(balance))
        return False
      case 4:
        total_income = self.IncomeOutput()
        print("Your total income is: " + str(total_income))
        return False
      case 5:
        total_expenses = self.ExpensesOutput()
        print("Your total expenses is: " + str(total_expenses))
        return False
      case 6:
        self.SeeFinanceHistory()
        return False
      case 7:
        self.GenerateReport()
        return False
      case 8:
        print("Returning to main menu...")
        return True
      case _:
        print("Invalid choice. Please try again.")
        return False