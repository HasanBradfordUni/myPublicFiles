from accounts import Accounts
from account import Account
from financeOptions import FinanceOptions
import getpass

class Menu:
  def __init__(self):
    self.menuOptions = {1: "1. Create Account", 2: "2. Login to your account", 3: "3. Change your Password", 4: "4. Logout",
                        5: "5. Load accounts (admin)", 6: "6. Search for an account", 7: "7. Add an account (admin)",
                        8: "8. Remove an account (admin)", 9: "9. Update a password (admin)", 10: "10. Save accounts (admin)",
                        11: "11. Finance options", 12: "12. Add admin account (admin)", 13: "13. Exit"}
    self.accounts = Accounts()

  def displayMenu(self):
    print("Welcome to Finance Fulcrum, Below are the main menu options\n")
    for option in self.menuOptions.values():
      print(option)

  def getChoice(self):
    print("\nEnter your choice from the options above: ")
    choice = 0
    while choice not in self.menuOptions.keys():
      try:
        choice = int(input("Enter your choice: "))
      except ValueError:
        print("Invalid input. Please enter a number.")
    return choice

  def createAccount(self):
    print("You have selected: Creating an account")
    username = input("Enter a username: ")
    password = getpass.getpass(prompt="Enter a password in digits only: ")
    account = Account(username, password, "basic")
    self.accounts.add_account(account)
    print("Account created successfully.")

  def loginToAccount(self):
    print("You have selected: Login to your account")
    #Logging into account section (Contains while loop to ensure limited no. of tries)
    attempts = 5
    logged_in = False
    while logged_in == False and attempts > 0:
      print("You have", attempts, "attempts left to login")
      username = input("Enter username: ")
      thisAccount = self.accounts.get_account(username)
      password = getpass.getpass(prompt="Enter a password in digits only: ")
      if thisAccount is not None:
        logged_in = thisAccount.Login(username, password)
      else:
        print("Account not found.")
        create_account = input("Would you like to create an account? (y/n): ")
        if create_account.lower() == "y":
          self.createAccount()
        else:
          print("Returning to main menu...")
        break
      attempts -= 1
    if not logged_in and thisAccount is not None:
      print("Login failed. Account now temporarily locked.")

  def changePassword(self):
    print("You have selected: Change your password")
    username = input("Enter your username: ")
    password = getpass.getpass(prompt="Enter your old password (digits only): ")
    new_password = getpass.getpass(prompt="Enter your new password (digits only): ")
    if self.accounts.update_password(username, password, new_password):
      print("Password changed successfully.")
    else:
      print("Incorrect username or password.")

  def logout(self):
    print("You have selected: Logout")
    username = input("Confirm by entering your username: ")
    account = self.accounts.get_account(username)
    if account is not None:
      account.logout()
    else:
      print("Account not found. Cannot be logged out.")

  def loadAccounts(self):
    print("You have selected: Load accounts")
    filename = input("Enter the filename to load accounts from: ")
    self.accounts.load_accounts(filename)

  def searchForAccount(self):
    print("You have selected: Search for an account")
    username = input("Enter the username of the account to search for: ")
    account = self.accounts.get_account(username)
    if account is not None:
      print("Account found:")
      print("Username:", account.username)
      print("Encrypted Password:", account.password)
      print("Logged in:", account.logged_in)
    else:
      print("Account not found.")

  def addAccount(self):
    print("You have selected: Add an account")
    username = input("Enter the username of the new account: ")
    password = input("Enter the password of the new account: ")
    account = Account(username, password, "basic")
    self.accounts.add_account(account)
    print("Account added successfully.")

  def removeAccount(self):
    print("You have selected: Remove an account")
    username = input("Enter the username of the account to remove: ")
    if self.accounts.remove_account(username):
      print("Account removed successfully.")
    else:
      print("Account not found.")

  def updatePassword(self):
    print("You have selected: Update a password")
    username = input("Enter the username of the account to update: ")
    old_password = getpass.getpass(prompt="Enter the old password (digits only): ")
    new_password = getpass.getpass(prompt="Enter the new password (digits only): ")
    if self.accounts.update_password(username, old_password, new_password):
      print("Password updated successfully.")
    else:
      print("Incorrect username or password.")

  def saveAccounts(self):
    print("You have selected: Save accounts")
    filename = input("Enter the filename to save accounts to: ")
    self.accounts.save_accounts(filename)
    if self.accounts.get_account_count() > 0:
      print("Accounts downloaded successfully!")
    else:
      print("No accounts to download!")

  def openFinanceOptions(self):
    print("You have selected: Finance options")
    financeOptions = FinanceOptions()
    exit = False
    while not exit:
      financeOptions.displayMenu()
      choice = financeOptions.getChoice()
      exit = financeOptions.handleChoice(choice)
      print("\n")

  def addAdminAccount(self):
    print("You have selected: Adding an admin account")
    username = input("Enter the username of the admin account (existing or new): ")
    password = input("Enter the password of the admin account: ")
    self.accounts.add_admin_account(username, password)
    print("Admin account added successfully.")

  def exitProgram(self):
    print("You have selected: Exit")
    print("Thank you for using Finance Fulcrum. Have a great day!")

  def handleChoice(self, choice):
    print()
    match choice:
      case 1:
        self.createAccount()
        return False
      case 2:
        self.loginToAccount()
        return False
      case 3:
        self.changePassword()
        return False
      case 4:
        self.logout()
        return False
      case 5:
        self.loadAccounts()
        return False
      case 6:
        self.searchForAccount()
        return False
      case 7:
        self.addAccount()
        return False
      case 8:
        self.removeAccount()
        return False
      case 9:
        self.updatePassword()
        return False
      case 10:
        self.saveAccounts()
        return False
      case 11:
        self.openFinanceOptions()
        return False
      case 12:
        self.addAdminAccount()
        return False
      case 13:
        self.exitProgram()
        return True
      case _:
        print("Invalid choice. Please try again.")
        return False