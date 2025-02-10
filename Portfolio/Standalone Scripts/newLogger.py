#A file that contains necessary and suplementary methods to 
# log output and errors from the program and store them
class general_logger():
  def __init__(self, filename):
    self.loggerFile = filename
    """The logger menu will contain the following options:
    1. Add to logs
    2. Search for logs
    3. Add Error to logs
    4. Search for errors in logs
    5. Exit
    """
    self.menu = {1: "1. Add to logs", 2: "2. Search for logs", 3: "3. Add Error to logs", 4: "4. Search for errors in logs", 5:"5. Add Input to logs", 6: "6. Search for inputs in logs", 7: "7. Exit"}

  def printMenu(self):
    print("\nMenu:")
    for key, value in self.menu.items():
      print(value)

  def getMenuOption(self):
    print("\nEnter your choice from the options above: ")
    choice = 0
    while choice not in self.menu.keys():
      try:
        choice = int(input("Enter your choice: "))
      except ValueError:
        print("Invalid input. Please enter a number.")
    return choice

  def cleanLoggerFile(self):
    logger = open(self.loggerFile, 'r')
    current_lines = ""
    for line in logger.readlines():
      if line != "\n":
        current_lines += line
    with open(self.loggerFile, 'w') as new_logger:
      new_logger.write(current_lines)

  def getLoggerFile(self):
    return self.loggerFile

  def changeLoggerFile(self, filename):
    self.loggerFile = filename

  def handleChoice(self, choice):
    print(f"You have chosen option {choice}")
    print()
    match choice:
      case 1:
        outputStatement = input("Enter the output statement: ")
        self.addToLogs(outputStatement)
        return False
      case 2:
        searchTerm = input("Enter the search term: ")
        self.searchForLogs(searchTerm)
        return False
      case 3:
        errorStatement = input("Enter the error statement: ")
        self.addToErrorLogs(errorStatement)
        return False
      case 4:
        searchTerm = input("Enter the search term: ")
        self.searchForErrors(searchTerm)
        return False
      case 5:
        inputPrompt = input("Enter the input prompt: ")
        inputStatement = input("Enter the input statement: ")
        self.addToInputLogs(inputPrompt, inputStatement)
        return False
      case 6:
        searchTerm = input("Enter the search term: ")
        self.searchForInputs(searchTerm)
        return False
      case 7:
        print("Exiting program...")
        return True
      case _:
        print("Invalid choice. Please try again.")
        return False

  def addToLogs(self, outputStatement):
    logger  = open(self.loggerFile, 'a')
    logger.write("Output:\n")
    outputStatement = outputStatement.replace("  ", "\n")
    logger.write(outputStatement+"\n")
    logger.close()

  def addToInputLogs(self, inputPrompt, inputStatement):
    logger  = open(self.loggerFile, 'a')
    logger.write("User Input:\n")
    logger.write(inputPrompt+" "+inputStatement+"\n")
    logger.close()

  def searchForInputs(self, searchTerm):
    logger = open(self.loggerFile, 'r')
    inputLines = []
    lineToAdd = False
    for lineNum, line in enumerate(logger):
      if line.startswith("Input:"):
        lineToAdd = True
      if lineToAdd:
        inputLines.append("Line Number "+str(lineNum)+": "+line)
      if line.startswith("Error:") or line.startswith("Output:"):
        lineToAdd = False
    logger.close()
    print(f"\nAll results containing {searchTerm} are below:\n")
    results = []
    for line in inputLines:
      if searchTerm in line:
        print(line)
        results.append(line)
    print(f"{len(results)} results found. You can now choose to narrow the search further or proceed!\n")
    narrowSearch = input("Do you wish to narrow the search further (Y/N)? ")
    if narrowSearch.lower() == 'y':
      newResults = []
      searchTerm = input("Enter the new search term: ")
      print(f"\nAll new results containing {searchTerm} are below:\n")
      for line in results:
        if searchTerm in line:
          print(line)
          newResults.append(line)
      print(f"{len(newResults)} new results found.")
      return newResults
    else:
      return results

  def searchForLogs(self, searchTerm):
    logger  = open(self.loggerFile, 'r')
    outputLines = []
    lineToAdd = False
    for lineNum, line in enumerate(logger):
      if line.startswith("Output:"):
        lineToAdd = True
      if lineToAdd:
        outputLines.append("Line Number "+str(lineNum)+": "+line)
      if line.startswith("Error:") or line.startswith("Input:"):
        lineToAdd = False
    logger.close()
    print(f"\nAll results containing {searchTerm} are below:\n")
    results = []
    for line in outputLines:
      if searchTerm in line:
        print(line)
        results.append(line)
    print(f"{len(results)} results found. You can now choose to narrow the search further or proceed!\n")
    narrowSearch = input("Do you wish to narrow the search further (Y/N)? ")
    if narrowSearch.lower() == 'y':
      newResults = []
      searchTerm = input("Enter the new search term: ")
      print(f"\nAll new results containing {searchTerm} are below:\n")
      for line in results:
        if searchTerm in line:
          print(line)
          newResults.append(line)
      print(f"{len(newResults)} new results found.")
      return newResults
    else:
      return results

  def searchForErrors(self, searchTerm):
    logger  = open(self.loggerFile, 'r')
    errorLines = []
    lineToAdd = False
    for lineNum, line in enumerate(logger):
      if line.startswith("Error:"):
        lineToAdd = True
      if lineToAdd:
        errorLines.append("Line Number "+str(lineNum)+": "+line)
      if line.startswith("Output:") or line.startswith("Input:"):
        lineToAdd = False
    logger.close()
    print(f"\nAll results containing {searchTerm} are below:\n")
    results = []
    for line in errorLines:
      if searchTerm in line:
        print(line)
        results.append(line)
    print(f"{len(results)} results found. You can now choose to narrow the search further or proceed!\n")
    narrowSearch = input("Do you wish to narrow the search further (Y/N)? ")
    if narrowSearch.lower() == 'y':
      newResults = []
      searchTerm = input("Enter the new search term: ")
      print(f"\nAll new results containing {searchTerm} are below:\n")
      for line in results:
        if searchTerm in line:
          print(line)
          newResults.append(line)
      print(f"{len(newResults)} new results found.")
      return newResults
    else:
      return results

  def addToErrorLogs(self, errorStatement):
    logger  = open(self.loggerFile, 'a')
    logger.write("Error:\n")
    errorStatement = errorStatement.replace("  ", "\n")
    logger.write(errorStatement+"\n")
    logger.close()

  def loggerMain(self):
    quitProgram = False
    print("Welcome to the official Akhtar Hasan logger program!")
    while not quitProgram:
      self.printMenu()
      choice = self.getMenuOption()
      quitProgram = self.handleChoice(choice)

if __name__ == "__main__":
  myLogger = general_logger("Other AI Projects/AI Document Extraction/src/localFiles/run_logs.txt")
  myLogger.loggerMain()