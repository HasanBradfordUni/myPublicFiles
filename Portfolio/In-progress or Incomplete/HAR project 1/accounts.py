from account import Account

class Accounts:
  def __init__(self):
    self.accounts = []

  def add_account(self, account):
    self.accounts.append(account)

  def get_account(self, username):
    for account in self.accounts:
      if account.username == username:
        return account
    return None

  def remove_account(self, username):
    for account in self.accounts:
      if account.username == username:
        self.accounts.remove(account)
        return True
    return False

  def update_password(self, username, old_password, new_password):
    for account in self.accounts:
      if account.username == username:
        if account.change_password(old_password, new_password):
          return True
    return False

  def get_all_accounts(self):
    return self.accounts

  def get_account_count(self):
    return len(self.accounts)

  def get_account_names(self):
    return [account.username for account in self.accounts]

  def get_account_passwords(self):
    return [account.password for account in self.accounts]

  def get_account_login_status(self):
    return [account.logged_in for account in self.accounts]

  def get_account_types(self):
    return [account.accountType for account in self.accounts]

  def get_account_info(self):
    return [(account.username, account.password, account.logged_in, account.accountType) for account in self.accounts]

  def save_accounts(self, filename):
    print("Saving accounts...")
    with open(filename, "w") as f:
      for account in self.accounts:
          f.write(f"{account.username},{account.password},{account.logged_in},{account.accountType}\n")
    print(len(self.accounts), "accounts saved successfully.")

  def load_accounts(self, filename):
    print("Loading accounts...")
    with open(filename, "r") as f:
      for line in f:
        username, password, logged_in, account_type = line.strip().split(",")
        account = Account(username, password, account_type)
        account.logged_in = logged_in
        self.add_account(account)
    print("Accounts loaded successfully.")
    print(len(self.accounts), "accounts loaded.")

  def add_admin_account(self, username, password):
    if username in self.get_account_names():
      account = self.get_account(username)
      if account.check_encrypted_password(password, account.password):
        account.set_account_type("admin")
        print("Admin account updated successfully.")
      else:
        print("Admin account failed to update.")
    else:
      admin_account = Account(username, password, "admin")
      self.accounts.append(admin_account)
      print("Admin account added successfully.")

  def get_admin_account(self):
    for account in self.accounts:
      if account.get_account_type() == "admin":
        return account
    return None
