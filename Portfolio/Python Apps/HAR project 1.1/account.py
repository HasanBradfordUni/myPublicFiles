from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Account:
  def __init__(self, username, password, accountType):
    self.username = username
    self.password = self.encrypt_password(password)
    self.logged_in = False
    self.accountType = accountType
    print("Welcome to Finance Fulcrum.")

  def Login(self, username, password):
    if username == self.username and self.check_encrypted_password(password, self.password):
      print("You are now logged in.")
      self.logged_in = True
    else:
      print("Incorrect information typed")
      self.logged_in = False
    return self.logged_in

  def encrypt_password(self, password):
    return pwd_context.hash(password)

  def check_encrypted_password(self, password, hashed):
    return pwd_context.verify(password, hashed)

  def change_password(self, old_password, new_password):
    if self.check_encrypted_password(old_password, self.password):
      self.password = self.encrypt_password(new_password)
      print("Password has been changed.")
      return True
    else:
      print("Incorrect password.")
      return False

  def logout(self):
    self.logged_in = False
    print("You have been logged out.")

  def get_account_type(self):
    return self.accountType

  def set_account_type(self, accountType):
    self.accountType = accountType

if __name__ == "__main__":
  username = "Bob"
  password = 102978932
  account = Account(username, password, "basic")

  user_username = input("Enter username: ")
  user_password = int(input("Enter a password (must be in digits): "))
  account.Login(user_username, user_password)
  account.change_password(user_password, 123456789)
  account.logout()
  account.Login(user_username, 123456789)
  print(account.get_account_type()) 