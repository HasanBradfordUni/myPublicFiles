class PersonalFinanceTracker:
    def __init__(self):
        self.income = 0
        self.expenses = 0
        self.savings_goal = 0
    
    def record_income(self, amount):
        self.income += amount
    
    def record_expense(self, amount):
        self.expenses += amount
    
    def set_savings_goal(self, amount):
        self.savings_goal = amount
    
    def view_summary(self):
        print("Personal Finance Summary:")
        print("-------------------------")
        print(f"Income: ${self.income}")
        print(f"Expenses: ${self.expenses}")
        print(f"Savings Goal: ${self.savings_goal}")
        print(f"Remaining to reach savings goal: ${self.savings_goal - self.income + self.expenses}")


def main():
    tracker = PersonalFinanceTracker()
    
    while True:
        print("\n1. Record Income")
        print("2. Record Expense")
        print("3. Set Savings Goal")
        print("4. View Summary")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            amount = float(input("Enter income amount: "))
            tracker.record_income(amount)
        elif choice == '2':
            amount = float(input("Enter expense amount: "))
            tracker.record_expense(amount)
        elif choice == '3':
            amount = float(input("Enter savings goal amount: "))
            tracker.set_savings_goal(amount)
        elif choice == '4':
            tracker.view_summary()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
