#Reporting

from datetime import *

class Reporting(): #ID = hastag with 5 digit number after it (e.g #71692)
  def __init__(self):
    self.ID_LIST = [] #1 to 1 mapping with finance history
    self.DATES_ID_MAPPING = {} #Mapping of IDs and dates, IDs as keys, and dates as values

  def setDate(self, transactionDate):
    self.ID_LIST_length = len(self.ID_LIST)

    if self.ID_LIST_length <= 0:  # Handles empty list case, considering edge cases of negative length
        self.NEW_ID = '#00000'  # Default starting ID
    else:
        last_item_number = self.ID_LIST[-1][1:6]  # Extract numeric part, excluding '#'
        # Preserve leading zeros in ID
        non_zero_index = next((i for i, c in enumerate(last_item_number) if c != '0'), 5)
        # Special case for transitioning from '#00000' to '#00001'
        if non_zero_index == 5 and self.ID_LIST[-1] == '#00000':
            self.NEW_ID = '#00001'
        else:
            self.NEW_ID = f"#{'0' * non_zero_index}{int(last_item_number) + 1}"
    
    self.ID_LIST.append(self.NEW_ID)
    self.DATES_ID_MAPPING[self.NEW_ID] = str(transactionDate)

  def getDate(self, transactionID):
    return self.DATES_ID_MAPPING[transactionID]

  def getID(self, index):
    return self.ID_LIST[index]

  def generateReport(self, startDate, endDate, financeHistory):
    self.datedTransactions = []
    self.transaction_list = financeHistory
    self.totalExpenses, self.totalIncome = 0, 0
    self.dSt, self.mSt, self.YSt = startDate.split("/")
    self.dEnd, self.mEnd, self.YEnd = endDate.split("/")
    self.stDate = date(int(self.YSt), int(self.mSt),int(self.dSt))
    #print(self.stDate)
    self.enDate = date(int(self.YEnd), int(self.mEnd), int(self.dEnd))
    for num in range(0, len(self.transaction_list)):
      thisID = self.ID_LIST[num]
      thisDate = self.DATES_ID_MAPPING[thisID]
      self.Transaction = Transaction(thisDate, self.transaction_list[num], "", "")
      self.trD, self.trM, self.trY = self.Transaction.date.split("/")
      self.transactionDate = date(int(self.trY), int(self.trM), int(self.trD))
      if self.stDate <= self.transactionDate <= self.enDate:
        self.datedTransactions.append(self.Transaction)
        if self.transaction_list[num] < 0:
          self.totalExpenses += abs(self.transaction_list[num])
        else:
          self.totalIncome += self.transaction_list[num]
    return self.totalIncome, self.totalExpenses, self.datedTransactions

class Transaction():
  def __init__(self, date, amount, category, notes):
    self.date = date
    self.amount = amount
    self.category = category
    self.notes = notes

def testReporting():
  report = Reporting()
  financeHistory = [100, -200, 150, -50, -50, -100, 100, 120, 200]
  for transaction in financeHistory:
    thisDate = input("Enter the date of transaction: ")
    report.setDate(thisDate)
  report.generateReport("01/01/2025", "02/02/2025", financeHistory)
  print(report.datedTransactions)

testReporting()